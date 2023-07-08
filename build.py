#!/usr/bin/env python3

import argparse
import os
import io
import yaml
import distutils.spawn
import re

from enum import Enum

class Target(Enum):
    PDF="pdf"
    HTML="html"
    MARKDOWN="markdown"    
    LATEX="latex"

def _get_bibliographies(path) -> list[str] | None:
    try:
        with io.open(f"{os.path.dirname(path)}/metadata.yaml", "r") as stream:
            metadata = yaml.safe_load(stream)
            try:
                return metadata["bibliography"]
            except:
                return None
    except FileNotFoundError:
        return None

def _get_title(path) -> str | None:
    search_dir = path + "/" if os.path.isdir(path) else os.path.dirname(path)
     
    try:
        with io.open(f"{search_dir}/metadata.yaml", "r") as stream:
            metadata = yaml.safe_load(stream)

            try:
                return metadata["title"]
            except:
                print("Could not find key 'title' in metadata")
                return None
    except FileNotFoundError:
        print(f"Could not find file in path: {search_dir}")
        return None

def _any_to_filename(string: str):
    # keep alphanumeric
    filename = "".join(c for c in string if (c.isalnum() or c == " ")) 
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

    # convert target to filename
    if "." in target:
        filename = target
    else:
        document_title = _get_title(source)

        if document_title is not None:
            filename = _any_to_filename(document_title) + f".{target}"
        else:
            filename = os.path.splitext(os.path.basename(source))[0] + f".{target}"

    if os.path.isdir(source):
        return _build_folder(pandoc, source, filename, options)
    else:
        return _build_single(pandoc, source, filename, options)

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
    
    args = parser.parse_args()

    missing = check_prerequisites(args.pandoc)

    if not args.docker and len(missing) != 0:
        print("Not all dependencies could be found:", missing, 
              "\nPlease make sure they are all in the PATH.")


    exit(main(args.source, args.target, args.options, pandoc=args.pandoc, docker=args.docker))
