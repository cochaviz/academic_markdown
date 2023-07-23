#!/usr/bin/env python3

import argparse
import os
import io
import yaml
import re
import subprocess
import shutil

import logging
import glob

def _docker_in_container_warning(docker_option: bool) -> bool:
    if os.path.exists("/.dockerenv") and docker_option:
            logging.warning("""docker:Docker option seems to be enabled inside a
                            docker container. If you're in a docker container,
                            consider omitting this option.""")

def _open_metadata(path: str) -> dict[str, str] | None:
    assert os.path.isdir(path) # should not trigger

    # open the 
    with io.open(f"{path}/metadata.yaml", "r") as stream:
        metadata = yaml.safe_load(stream)
        return metadata

def _open_frontmatter(path: str) -> dict[str, str] | None:
    if os.path.isdir(path):
        raise ValueError("Dirs do not have frontmatters")

    import frontmatter

    if not frontmatter.checks(path):
        raise AttributeError("File does not contain frontmatter")

    return frontmatter.load(path)

def _get_metadata(path: str, property: str | None = None ) -> str | None:
    search_dir = path + "/" if os.path.isdir(path) else os.path.dirname(path) + "/"
    metadata = None

    # first try getting the metadata.yaml file
    try:
        metadata = _open_metadata(search_dir)
    except FileNotFoundError as e:
        logging.info(f"metadata: Could not find metadata.yaml in folder {search_dir}")

    # then look for frontmatter
    try:
        metadata = _open_frontmatter(path)
    except ValueError:
        logging.info(f"frontmatter: {path} is not a file")
    except ImportError:
        logging.warning(f"frontmatter: Module 'frontmatter' not installed, cannot read frontmatter from {path}")
    except FileNotFoundError as e:
        logging.warning(f"frontmatter: Could not find file {path}")
    except AttributeError:
        logging.info(f"frontmatter: File {path} does not contain frontmatter")

    # if we have a metadata file and are looking for a specific property
    if metadata is not None and property is not None:
        try:
            return metadata[property]  
        except KeyError:
            logging.error(f"Metadata: Property {property} could not be found in metadata")
    return metadata
        
def _title_to_filename(title: str):
    # keep alphanumeric
    filename = "".join(c for c in title if (c.isalnum() or c == " ")) 
    # remove any spaces and replace with underscore
    filename = re.sub("\ +", "_", filename)
    # make lowercase
    filename = filename.lower()

    return filename

def check_in_path(dependencies: list[str]) -> None | list[str]:
    missing = []

    for dependency in dependencies:
            if shutil.which(dependency) is None:
                missing.append(dependency)
            
    return missing

def _build_single(pandoc: list[str], source: str, filename: str, options: list[str]):
    metadata_file = f"{os.path.dirname(source)}/metadata.yaml"

    if os.path.exists(metadata_file):
        options.append(f"--metadata-file={metadata_file}")

    return subprocess.run([*pandoc, "-F", "pandoc-crossref", "--citeproc",
                    "--from=markdown+mark", *options, source, "-o", filename]) 

def _build_folder(pandoc: list[str], source: str, filename: str, options: list[str]):

    return subprocess.run([*pandoc, "-F", "pandoc-crossref", "--citeproc", 
                           f"--metadata-file={source}/metadata.yaml", "--from=markdown+mark", 
                           *options, *glob.glob(f"{source}/*.md"), f"--output={filename}"])

def main(source: str, target: str, 
         options: str = "", docker: bool = False, 
         pandoc: str = "pandoc", tectonic: bool = False):
        
    if docker:
        _docker_in_container_warning(docker)
        pwd = os.getcwd()
        pandoc = ["docker", "run", "--mount", f"type=bind,source={pwd},target=/var/data", 
                  "--workdir=/var/data", "cochaviz/academic_markdown"]
    else:
        pandoc = [pandoc]
    
    # set source to file if folder contains only one file
    if os.path.isdir(source):
        markdown_in_folder = glob.glob(f"{source}/*.md")
        
        if len(markdown_in_folder) == 1:
            source = markdown_in_folder[0]
            logging.info(f"Only one file was found in given folder, \
                updating source to {source}")

    # set options
    if "md" in target:
        options.append("--to=gfm")

    if not "md" in target and os.path.isfile(source):
        options.append("--shift-heading-level=-1")

    if "tex" in target:
        options.append("-s")

    # convert target to filename
    if "." in target:
        out_filename = target
    else:
        document_title = _get_metadata(source, "title")

        if document_title is not None:
            out_filename = _title_to_filename(document_title) + f".{target}"
        else:
            out_filename = f"{os.path.splitext(os.path.basename(source))[0]}.{target}"

    if tectonic or docker:
        options.append("--pdf-engine=tectonic")

    logging.info(f"Writing to {out_filename}...")

    if os.path.isdir(source):
        if _build_folder(pandoc, source, out_filename, options) != 0:
            exit(1)
    else:
        if _build_single(pandoc, source, out_filename, options) != 0:
            exit(1)

    return out_filename

if __name__=="__main__":
    parser = argparse.ArgumentParser(prog="build.py", description=
                                     """Wrapper for `pandoc` providing sensible
                                     defaults for rendering from pandoc-flavored
                                     markdown used in academic writing.""") 
    parser.add_argument("source", help=
                        """Source file or folder. In the case that the source is
                        a single file, also mention the extension
                        (your_file.md).""") 
    parser.add_argument("target", help="""
                        Target output file, or extension (pdf, md, tex, etc.). Uses
                        pandoc under the hood, so refer to their documentation
                        for the options.""")
    parser.add_argument("--options", default="", type=list[str], help=
                        """Additional options to pass through to pandoc.""")
    parser.add_argument("--pandoc", default="pandoc", type=str, help=
                        """Path to pandoc in case it cannot be provided through the
                        PATH variable. Gets overridden if the --docker option is
                        set.""")
    parser.add_argument("--docker", action="store_true", help=
                        """Use docker configuration to build, requires docker to
                        be installed.""")
    parser.add_argument("--log", type=str, help=
                        """Log level (ERROR, WARNING, INFO, DEBUG). Default is WARNING.""")
    parser.add_argument("--do-not-open", action="store_true", help=
                        """Do not open output in default code.""")
    parser.add_argument("--tectonic", action="store_true", help=
                        """Use tectonic when creating PDFs to install
                        missing packages on the fly. Is ignored when docker is
                        used.""")
    
    args = parser.parse_args()

    # not using docker means we have to check dependencies
    if not args.docker:
        dependencies = [
            args.pandoc,
            "pandoc-crossref",
            "pdflatex",
        ]

        if args.tectonic:
            dependencies.append("tectonic")

        missing = check_in_path(dependencies)

        if len(missing) != 0:
            logging.critical(f"Not all dependencies could be found: {missing}. \
                Please ensure they are all in the PATH.")
            exit(1)

    # enabling logging
    if args.log:
        numeric_level = getattr(logging, args.log.upper(), "WARNING")

        if not isinstance(numeric_level, int):
            raise ValueError(f"Invalid log level: {args.log}")

        logging.basicConfig(level=numeric_level)

    logging.debug("Debugging 🤓")

    out_filename = main(
        args.source, args.target, 
        args.options, 
        pandoc=args.pandoc, docker=args.docker,
        tectonic=args.tectonic
    )

    # open created file first by trying to open in VSCode, then with the
    # default pdf reader. Not sure whether this should be the other way around
    if not args.do_not_open:
        try:
            subprocess.run(["code", out_filename])
        except FileNotFoundError:
            try:
                subprocess.run(["xdg-open", out_filename])
            except FileNotFoundError:
                logging.warning(f"Could not open {out_filename} using either 'code' or 'xdg-open'") 
                exit(0)
