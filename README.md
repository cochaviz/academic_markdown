# Academic Markdown - Tools and Guide

This repository contains my workflow for using markdown and pandoc for academic
writing and serves as a template for that workflow. If you're just looking to
try it out, press the green button that says _Use This Template_ and open in a
codespace.  Otherwise, continue reading to set up a more permanent version of
this environment.

In this README, you will find instructions on how to use `build.py` and the
provided `Dockerfile`. That is, how to set up your system to successfully build
markdown files to `pdf`, $\LaTeX$, `HTML`, and markdown (that is
Github-flavoured markdown with rendered citations).

In _Workflow_, I will show how I use this repository and VSCode in conjunction
with Zotero to write articles, surveys, etc. This is available in both
[pdf](./academic_markdown.pdf) and [markdown](./academic_markdown.md) format, of
which the source can be found in `src/`.

## Quick Start

To start, you can choose to:

- [Use the provided Dockerfile](https://www.docker.com/) to set up a Docker
container

- Install the required dependencies ([`Python (3.11)`](https://www.python.org/),
[`pandoc`](https://pandoc.org/),
[`pandoc-crossref`](https://github.com/lierdakil/pandoc-crossref), and
[$\LaTeX$](https://www.latex-project.or/)) yourself

- Open this template in a Github codespace (green button in the top-right of the
repository)

- [Open locally in a VSCode
devcontainer](https://vscode.dev/redirect?url=vscode://ms-vscode-remote.remote-containers/cloneInVolume?url=https://github.com/cochaviz/academic_markdown).

If you are on Github, using codespaces is definitely the easiest if you'd just
like to have a look around.

### Building

When using VSCode, there are [Build
tasks](https://code.visualstudio.com/Docs/editor/tasks) that can be run to build
the files according to the current folder structure. This is just a proxy for
`build.py`, and can also be run manually.

In case you'd like to build manually, refer to the usage of `build.py` in the
command line:

```bash
$ ./build.py -h
usage: build.py [-h] [--options OPTIONS] [--pandoc PANDOC] [--docker] source target

Wrapper for `pandoc` providing sensible defaults for rendering from pandoc-flavored markdown used in academic writing.

positional arguments:
  source             Source file or folder. In the case that the source is a single file, also mention the extension (your_file.md).
  target             Target file and extension (e.g. my_project.pdf). Uses pandoc under the hood, so refer to their documentation for the options. This build file has preselected options for markdown, LaTeX, and PDF files.

options:
  -h, --help         show this help message and exit
  --options OPTIONS  Additional options to pass through to pandoc.
  --pandoc PANDOC    Path to pandoc in case it cannot be provided through the PATH variable. Gets overridden if the --docker option is set.
  --docker           Use docker configuration to build, requires docker to be installed.
```

## Capabilities

For my writing, I wanted to be able to do the following things:

- Work locally (preferably VSCode)
- Reference citations from a `.bib` file
- Use figures with captions
- Use common journal $\LaTeX$ templates
- Export to $\LaTeX$, `markdown`, and pdf

This repository is my attempt at making an academic writing workflow that is as
frictionless as possible without losing the configurability provided by the used
tools.
