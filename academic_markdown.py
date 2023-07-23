#!/usr/bin/env python3

import argparse
import os
import io
import yaml
import re
import subprocess
import shutil
import shlex

import logging
import glob

def _open_file(filename: str):
    # open file first by trying to open in VSCode, then with the
    # default pdf reader. Not sure whether this should be the other way around

    try:
        subprocess.run(["code", filename], check=True)
    except subprocess.CalledProcessError:
        try:
            subprocess.run(["xdg-open", filename], check=True)
        except subprocess.CalledProcessError:
            logging.warning(f"Could not open {filename} using either 'code' or 'xdg-open'") 

def _set_verbosity(level: str):
    numeric_level = getattr(logging, level.upper(), "WARNING")

    if not isinstance(numeric_level, int):
        raise ValueError(f"Invalid log level: {level}")

    logging.basicConfig(level=numeric_level)

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

def main(source: str, target: str, 
         options: str = "", docker: bool = False, 
         pandoc: str = "pandoc", tectonic: bool = False):
        
    if docker:
        _docker_in_container_warning(docker)
        pandoc = shlex.split(f"docker run \
            --mount type=bind,source={os.getcwd()},target=/var/data \
            --workdir=/var/data \
            cochaviz/academic_markdown")
    else:
        pandoc = shlex.split(pandoc)
    
    # source always refers to the folder which is being built
    if os.path.isdir(source):
        source_files = glob.glob(f"{source}/*.md")
    else:
        source = os.path.dirname(source)
        source_files = [source]

    # all resources should be located in the source folder
    options.append(f"--resource-path={source}")

    # set options
    if "tex" in source_files[0]:
        logging.info("Using latex defaults")
        options.append("--defaults=config/latex.yaml")
    if "md" in source_files[0]:
        options += [
            "--from=markdown+mark",
            "--filter=pandoc-crossref",
            "--citeproc",
        ]

        if len(source_files) > 1:
            options.append(f"--metadata-file={source}/metadata.yaml")
        if len(source_files) == 1 and "md" not in target:
            options.append(f"--shift-heading-level=-1")
        if "md" in target:
            options.append("--to=gfm")
        if "tex" in target:
            options.append("--standalone")

    # if docker is used, set tectonic option by default
    if (tectonic or docker) and "pdf" in target:
        options.append("--pdf-engine=tectonic")

    # convert target to filename (if it isn't already)
    if "." in target:
        out_filename = target
    else:
        document_title = _get_metadata(source, "title")

        if document_title is not None:
            out_filename = f"{_title_to_filename(document_title)}.{target}"
        else:
            intermediate_filename = os.path.basename(
                source if len(source_files) > 1 else source_files[0]
                )
            out_filename = f"{os.path.splitext(intermediate_filename)[0]}.{target}"

    out_filename = f"{os.getcwd()}/{out_filename}"

    logging.info(f"Writing to {out_filename}...")

    pandoc_command = [
        *pandoc, *options, *source_files, 
        f"--output={out_filename}"
    ]

    pandoc_command_string = " ".join(pandoc_command)
    logging.debug(f"Running pandoc command:\n\n{pandoc_command_string}")

    process = subprocess.run(pandoc_command) 

    if process.returncode != 0:
        logging.error(f"pandoc: Exited unexpectedly: {process.stderr}")
        exit(process.returncode)

    return out_filename

if __name__=="__main__":
    parser = argparse.ArgumentParser(prog="build.py", description=
                                     """Wrapper for `pandoc` providing sensible
                                     defaults for rendering from pandoc-flavored
                                     markdown used in academic writing.""") 
    parser.add_argument("source", 
                        help="""Source file or folder. In the case that the source is
                        a single file.""") 
    parser.add_argument("target", 
                        help="""Target output file, or extension (pdf, md, tex, etc.). Uses
                        pandoc under the hood, so refer to their documentation
                        for the options.""")
    parser.add_argument("--options", default="", type=list[str], 
                        help="""Additional options to pass through to pandoc.""")
    parser.add_argument("--pandoc", default="pandoc", type=str, 
                        help="""Path to pandoc in case it cannot be provided through the
                        PATH variable. Gets overridden if the --docker option is
                        set.""")
    parser.add_argument("--docker", action="store_true", 
                        help="""Use docker configuration to build, requires docker to
                        be installed.""")
    parser.add_argument("--verbosity", type=str, choices=["ERROR", "WARNING", "INFO", "DEBUG"], 
                        default="WARNING",
                        help="""Set verbosity level. Default is WARNING.""")
    parser.add_argument("--do-not-open", action="store_true", 
                        help="""Do not open output in default code.""")
    parser.add_argument("--tectonic", action="store_true", 
                        help="""Use tectonic when creating PDFs to install
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

    # set verbosity level
    _set_verbosity(args.verbosity)

    logging.debug("Debugging 🤓")

    out_filename = main(
        args.source, args.target, 
        args.options, 
        pandoc=args.pandoc, docker=args.docker,
        tectonic=args.tectonic
    )

    if not args.do_not_open:
        _open_file(out_filename)