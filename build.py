#!/usr/bin/env python3

import argparse
import os
import io
import yaml
import distutils.spawn

def get_bibliographies(path) -> list[str]:
    with io.open(f"{os.path.dirname(path)}/metadata.yaml", "r") as stream:
        metadata = yaml.safe_load(stream)
        return metadata["bibliography"]

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

def _build_single(pandoc: str, source: str, target: str, options: str):
    metadata_file = f"{os.path.dirname(source)}/metadata.yaml"

    if os.path.exists(metadata_file):
        options += f" --metadata-file={metadata_file}"

    return os.system(f"{pandoc} -F pandoc-crossref --citeproc {options} -i {source} -o {target}") 

def _build_folder(pandoc: str, source: str, target: str, options: str):
    return os.system(f"{pandoc} -F pandoc-crossref --citeproc {options} \
    --metadata-file={source}/metadata.yaml -i {source}/*.md -o {target}")

def main(source: str, target: str, options: str = "", docker: bool = False, pandoc: str = "pandoc"):
    if docker:
        pandoc = 'docker run --mount type=bind,source="$(pwd)",target=/var/data --workdir /var/data pandoc/extra'

    if target.split(".")[-1] == "md":
        options += " -s -f gfm"
    if target.split(".")[-1] == "tex":
        options += " -s"

    if os.path.isdir(source):
        return _build_folder(pandoc, source, target, options)
    else:
        return _build_single(pandoc, source, target, options)

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
                        Target file and extension (e.g. my_project.pdf). Uses
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
