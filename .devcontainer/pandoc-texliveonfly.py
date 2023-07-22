#!/usr/bin/env python

import sys
import subprocess
import glob
import shutil

def _set_extension_tex(filename: str) -> str:
    return ".".join(filename.split('.')[:-1] + ["tex"])

def _get_opt_value(option: str) -> str:
    try:
        return sys.argv[sys.argv.index(option) + 1]
    except ValueError:
        return ""

def _set_opt_value(option: str, value: str) -> list[str]:
    args = sys.argv
    args[args.index(option) + 1] = value
    return args

def _run_default():
    return subprocess.run(["pandoc", *sys.argv[1:]]).returncode

if __name__=="__main__":
    is_pdf = True

    if not shutil.which("texliveonfly") or "--disable-onfly":
        exit(_run_default())

    if _get_opt_value("-t") == "pdf":
        argv =  _set_opt_value("-t", "tex")
        subprocess.run(["pandoc", "-s", *argv[1:]]) 
    elif ".pdf" in _get_opt_value("-o"):
        new_filename = _set_extension_tex(_get_opt_value("-o"))
        argv = _set_opt_value("-o", new_filename)
        subprocess.run(["pandoc", "-s", *argv[1:]])
    elif ".pdf" in sys.argv[-1]:
        new_filename = _set_extension_tex(sys.argv[-1])
        subprocess.run(["pandoc", "-s", *sys.argv[1:-1], new_filename])
    else:
        is_pdf = False

    if is_pdf:
        exit(subprocess.run(["texliveonfly", *glob.glob("*.tex")]).returncode)
    else:
        exit(_run_default())