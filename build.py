#!/usr/bin/env python3

import argparse
import os
import io
import yaml
import distutils.spawn
import re

import logging
import glob

from enum import Enum

class Target(Enum):
    PDF="pdf"
    HTML="html"
    MARKDOWN="markdown"    
    LATEX="latex"

def _open_metadata(path: str) -> dict[str, str] | None:
    assert os.path.isdir(path) # should not be hit

    with io.open(f"{os.path.dirname(path)}/metadata.yaml", "r") as stream:
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

    try:
        metadata = _open_metadata(search_dir)
    except FileNotFoundError as e:
        logging.info(f"Metadata: Could not find metadata.yaml in folder {search_dir}")

    try:
        metadata = _open_frontmatter(path)
    except ValueError:
        logging.info(f"Frontmatter: {path} is not a file")
    except ImportError:
        logging.warning(f"Frontmatter: Module 'frontmatter' not installed, cannot read frontmatter from {path}")
    except FileNotFoundError as e:
        logging.warning(f"Frontmatter: Could not find file {path}")
    except AttributeError:
        logging.info(f"Frontmatter: File {path} does not contain frontmatter")

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

def check_prerequisites(pandoc: str) -> None | list[str | list[str]]:
    dependencies = [
        pandoc,
        "pandoc-crossref",
        ["pdflatex", "xelatex"]
    ]

    missing = []

    for dependency in dependencies:
        if isinstance(dependency, list):
            possible_available = []

            for possible_dependency in dependency:
                if distutils.spawn.find_executable(possible_dependency):
                    possible_available.append(possible_dependency)
                    break
            if possible_available == 0:
                missing.append(dependency)
        else:  
            if not distutils.spawn.find_executable(dependency):
                missing.append(dependency)
            
    return missing

def _build_single(pandoc: str, source: str, filename: str, options: str):
    metadata_file = f"{os.path.dirname(source)}/metadata.yaml"

    if os.path.exists(metadata_file):
        options += f" --metadata-file={metadata_file}"

    return os.system(f"{pandoc} -F pandoc-crossref --citeproc \
                    -f markdown {options} {source} -o {filename}") 

def _build_folder(pandoc: str, source: str, filename: str, options: str):
    return os.system(f"{pandoc} -F pandoc-crossref --citeproc --metadata-file={source}/metadata.yaml \
                     -f markdown {options} {source}/*.md -o {filename}")

def main(source: str, target: str, options: str = "", docker: bool = False, pandoc: str = "pandoc"):
    if docker:
        pandoc = 'docker run --mount type=bind,source="$(pwd)",target=/var/data --workdir /var/data pandoc/extra'

    if "md" in target:
        options += "-t gfm"
    
    # set source to file if folder contains only one file
    if os.path.isdir(source):
        markdown_in_folder = glob.glob(f"{source}/*.md")
        
        if len(markdown_in_folder) == 1:
            source = markdown_in_folder[0]
            logging.info(f"Only one file was found in given folder, updating source to {source}")

    # convert target to filename
    if "." in target:
        out_filename = target
    else:
        document_title = _get_metadata(source, "title")

        if document_title is not None:
            out_filename = _title_to_filename(document_title) + f".{target}"
        else:
            out_filename = f"{os.path.splitext(os.path.basename(source))[0]}.{target}"

    if os.path.isdir(source):
        return _build_folder(pandoc, source, out_filename, options)
    else:
        return _build_single(pandoc, source, out_filename, options)

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
                        for the options. This build file has preselected options
                        for markdown, LaTeX, and PDF files.""")
    parser.add_argument("--options", default="", type=str, help=
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
    
    args = parser.parse_args()

    missing = check_prerequisites(args.pandoc)

    if not args.docker and len(missing) != 0:
        logging.critical("Not all dependencies could be found:", missing, 
              "\nPlease ensure they are all in the PATH.")
        exit(1)

    if args.log:
        numeric_level = getattr(logging, args.log.upper(), "WARNING")

        if not isinstance(numeric_level, int):
            raise ValueError(f"Invalid log level: {args.log}")

        logging.basicConfig(level=numeric_level)

    logging.debug("Debugging 🤓")
    exit(main(args.source, args.target, args.options, pandoc=args.pandoc, docker=args.docker))
