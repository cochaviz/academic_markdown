# Academic Markdown - Tools and Guide

[![Open in Dev
Containers](https://img.shields.io/static/v1?label=Dev%20Containers&message=Open&color=blue&logo=visualstudiocode)](https://vscode.dev/redirect?url=vscode://ms-vscode-remote.remote-containers/cloneInVolume?url=https://github.com/cochaviz/academic_markdown)

This repository contains my workflow for using markdown and `pandoc` for
academic writing and serves as a template for that workflow. If you’re
just looking to try it out, press the green button that says *Use This
Template* and open it in a codespace. Otherwise, continue reading to set
up a more permanent version of this environment.

In this README, you will find instructions on how to use `build.py` and
the provided `Dockerfile`. That is, how to set up your system to
successfully build markdown files to `pdf`, $\LaTeX$, `HTML`, and
markdown (that is Github-flavoured markdown with rendered citations).

In *Workflow*, I will show how I use this repository and VSCode in
conjunction with Zotero to write articles, surveys, etc. This is
available in both [pdf](./academic_markdown.pdf) and
[markdown](./academic_markdown.md) format, of which the source can be
found in `src/`.

## Capabilities

For my writing, I wanted to be able to do the following things:

- Work locally (preferably VSCode).
- Write academic papers and reports (e.g. work with Zotero and create
  figures).
- Create $\LaTeX$, `markdown`, and pdf files.
- Focus on writing, not on markup.

My conclusion was that writing in markdown and using `pandoc` to export
was the way to go. This repository is my attempt at making a workflow
that satisfies these conditions. Furthermore, I hope to provide a
foundation for people to start exploring all these amazing tools that
are available *for free*.

## Quick Start

To start, you can choose to:

- [Use the provided Dockerfile](https://www.docker.com/) to create a
  container in which the files are built (use the `--docker` flag).

- Install the required dependencies ([Python
  (3.11)](https://www.python.org/), [`pandoc`](https://pandoc.org/),
  [`pandoc-crossref`](https://github.com/lierdakil/pandoc-crossref), and
  [LaTeX](https://www.latex-project.or/)) yourself.

- Open this template in a Github codespace (green button in the
  top-right of the repository).

- Open locally in a VSCode
  [devcontainer](https://vscode.dev/redirect?url=vscode://ms-vscode-remote.remote-containers/cloneInVolume?url=https://github.com/cochaviz/academic_markdown).

If you are on Github, using codespaces is definitely the easiest if
you’d just like to have a look around. Be aware that this might take a
while to set up (about 2 minutes), but only needs to be done once.

### Building

When using VSCode, there are [Build
tasks](https://code.visualstudio.com/Docs/editor/tasks) that automate
this process *based on the currently opened file*. This is just a proxy
for `academic_markdown.py`, and can also be run manually.

In case you’d like to build manually, refer to the usage of
`academic_markdown.py` in the command line.

``` txt
$ python academic_markdown.py -h

usage: academic_markdown.py [-h] {build,check-health} ...

Wrapper for `pandoc` providing sensible defaults for rendering from pandoc-flavored markdown used in academic writing.

positional arguments:
  {build,check-health}
    build               Build document or set of documents through pandoc.
    check-health        Check if all the necessary executables are available and properly configured

options:
  -h, --help            show this help message and exit
```

Specifically, the `build` sub-command.

``` txt
$ python academic_markdown.py build -h

usage: academic_markdown.py build [-h] [--options OPTIONS] [--pandoc PANDOC] [--docker] [--check-health] [--verbosity {ERROR,WARNING,INFO,DEBUG}] [--do-not-open] [--tectonic] source target

positional arguments:
  source                Source file or folder. In the case that the source is a single file.
  target                Target output file, or extension (pdf, md, tex, etc.). Uses pandoc under the hood, so refer to their documentation for the options.

options:
  -h, --help            show this help message and exit
  --options OPTIONS     Additional options to pass through to pandoc.
  --pandoc PANDOC       Path to pandoc in case it cannot be provided through the PATH variable. Gets overridden if the --docker option is set.
  --docker              Use docker configuration to build, requires docker to be installed.
  --check-health        Check if dependencies are installed. If docker flag is set, it will only check whether docker requirement are met.
  --verbosity {ERROR,WARNING,INFO,DEBUG}
                        Set verbosity level. Default is WARNING.
  --do-not-open         Do not open output in default code.
  --tectonic            Use tectonic when creating PDFs to install missing packages on the fly. Is ignored when docker is used.
```

For concrete example of how to use this, refer to the [VSCode
tasks](.vscode/tasks.json). Each of these tasks provides a different
example of how to use the script.

### Usage

Personally, I work a lot in VSCode meaning that this workflow is
optimized for use with that IDE in particular. All the required files
and instructions, however, are available in such a manner that this can
be set up similarly with any IDE.

#### Project Structure

I imagine two ways of writing which I have often encountered myself. The
first is a situation in which you only need to write a small report. The
second is a situation where multiple files are required for that single
final document to avoid one incredibly large document.

<div id="lst:single_file_setup" class="listing txt">

Listing 1: Setup with a single file. Since all the information can be
found in one file (besides perhaps the bibliography), `metadata.yaml` is
optional and front matter can also be used.

``` txt
├── academic_markdown.py
└── docs
    ├── my_report.md
    ├── bibliography.bib
    ├── images
    └── [metadata.yaml] // optional, preferrably use frontmatter
```

</div>

<div id="lst:multiple_file_setup" class="listing txt">

Listing 2: Setup with multiple files. Here, `pandoc` would use the
frontmatter of the first document, if available, but I think the
`metadata.yaml` should be provided. This separates configurations from
content in larger projects.

``` txt
├── academic_markdown.py
└── docs
    ├── 01_introduction.md
    ├── 02_methodology.md
    ├── 03_conclusion.md
    ├── bibliography.bib
    ├── images
    └── metadata.yaml
```

</div>

When using `academic_markdown.py`, these situations are determined by
the number of files in the target folder. When there is only one, the
first situation is assumed, and `metadata.yaml` is optional. When there
are more files, the second situation is assumed, and `metadata.yaml` is
required.

#### Integration with VSCode

- tasks

- links

- citations

- previewing

#### Other IDEs

## Motivation

My reasoning is as follows: Markdown is a great format to write in but
lacks configurability. $\LaTeX$ is great for configurability, but rather
hard to write in (updates take quite a while to render, and the syntax
is sometimes rather distracting). One should focus on writing first, and
then make small adjustments where necessary. For this reason, I first
write in Markdown and then convert to PDF through $\LaTeX$. In case I
would like to customize certain aspects of the exported file, I export
to $\LaTeX$ and then to pdf.

While all of this is supported by `pandoc`, finding a system to work
with this is not necessarily trivial. This repository should provide
everything necessary to make the above workflow as smooth as possible
while still allowing for personalization.

## Roadmap

- [x] **Dockerized Environment**. Lightweight dockerized environment
  that allows for a full replacement of `pandoc`. Also automatically
  downloads missing latex packages.

- [ ] **Predefined devcontainer**. This will prevent long waiting times
  for using a devcontainer both locally and in codespaces.

- [ ] **Github Actions for building**. Use GitHub Actions to
  automatically build to PDF, $\LaTeX$ according to user preferences.
  This could be useful for ensuring rendered documents are always
  up-to-date, and avoiding the necessity for local builds. Could,
  perhaps, also be faster than building locally and pushing.

- [ ] **Full Manual**. A complete and detailed explanation of how this
  workflow can be used. This should be an instruction for any person
  that would like to use markdown for serious writing. It should provide
  an introduction to `pandoc`, docker, and VSCode.

- [ ] **Independent VSCode Extension**. A VSCode extension, independent
  of `build.py`. This could be an improved user experience for existing
  VSCode users. This template should, however, still be as usable
  without VSCode.
