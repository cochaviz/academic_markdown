# Academic Markdown - Tools and Guide

This repository contains my workflow for using markdown and `pandoc` for
academic writing and serves as a template for that workflow. If you’re
just looking to try it out, press the green button that says *Use This
Template* and open it in a codespace. Otherwise, continue reading to set
up a more permanent version of this environment.

In this README, you will find instructions on how to use
`academic_markdown` and the provided `Dockerfile`. That is, how to set
up your system to successfully build markdown files to `pdf`, LaTeX,
`HTML`, and markdown (that is Github-flavoured markdown with rendered
citations).

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
- Create LaTeX, `markdown`, and pdf files.
- Focus on writing, not on markup.

My conclusion was that writing in markdown and using `pandoc` to export
was the way to go. This repository is my attempt at making a workflow
that satisfies these conditions. Furthermore, I hope to provide a
foundation for people to start exploring all these amazing tools that
are available *for free*.

## Quick Start

To start, you can choose to:

- [Use the provided Dockerfile](https://www.docker.com/) to create a
  container in which the files are built (use the `--docker` flag), in
  conjunction with the `academic_markdown` command line interface.

- Install the required dependencies ([Python
  (3.11)](https://www.python.org/), [`pandoc`](https://pandoc.org/),
  [`pandoc-crossref`](https://github.com/lierdakil/pandoc-crossref), and
  [LaTeX](https://www.latex-project.or/)), etc. yourself. (Check
  `academic_markdown check-health` for the requirements).

- Open this template in a Github codespace (green button in the
  top-right of the repository).

- Open locally in a VSCode
  [devcontainer](https://vscode.dev/redirect?url=vscode://ms-vscode-remote.remote-containers/cloneInVolume?url=https://github.com/cochaviz/academic_markdown).

If you are on Github, using codespaces is definitely the easiest if
you’d just like to have a look around. Be aware that this might take a
while to set up (about 2 minutes), but only needs to be done once.

If you’re not directly using the devcontainer, you’ll have to install
the `academic_markdown` cli yourself with

``` shell
python3 -m pip install academic_markdown
```

### Building

When using VSCode, there are [Build
tasks](https://code.visualstudio.com/Docs/editor/tasks) that automate
this process *based on the currently opened file*. This is just a proxy
for `academic_markdown`, and can also be run manually.

In case you’d like to build manually, refer to the usage of
`academic_markdown` in the command line.

``` txt
Usage: academic_markdown [OPTIONS] COMMAND [ARGS]...                                                          
                                                                                                               
╭─ Options ───────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --install-completion          Install completion for the current shell.                                     │
│ --show-completion             Show completion for the current shell, to copy it or customize the            │
│                               installation.                                                                 │
│ --help                        Show this message and exit.                                                   │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ──────────────────────────────────────────────────────────────────────────────────────────────────╮
│ build                                                                                                       │
│ check-health                                                                                                │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

Specifically, the `build` sub-command.

``` txt
╭─ Arguments ─────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    source      TEXT  [default: None] [required]                                                           │
│ *    target      TEXT  [default: None] [required]                                                           │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ───────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --options                                TEXT                                                               │
│ --docker           --no-docker                 [default: no-docker]                                         │
│ --pandoc                                 TEXT  [default: pandoc]                                            │
│ --tectonic         --no-tectonic               [default: no-tectonic]                                       │
│ --open-rendered    --no-open-rendered          [default: no-open-rendered]                                  │
│ --help                                         Show this message and exit.                                  │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

For concrete examples of how to use this, refer to the [VSCode
tasks](.vscode/tasks.json). Each of these tasks provides a different
example of how to use the script.

### Usage

Personally, I work a lot in VSCode meaning that this workflow is
optimized for use with that IDE in particular. All the required files
and instructions, however, are available in such a manner that this can
be set up similarly with any IDE.

#### Project Structure

I imagine two ways of writing which I have often encountered myself. The
first is a situation in which you only need to write one or multiple
smaller reports (see lst. 1). The second is a situation where multiple
files are required for that single final document to avoid one
incredibly large document (see lst. 2).

<div id="lst:single_file_setup" class="listing bash">

Listing 1: Setup with a single file. Metadata regarding the markdown
files can be found in their respective frontmatter. When building a
‘folder’ without a `metadata.yaml` all the files will be rendered
separately.

``` bash
├── .devcontainer
├── .vscode
└── docs
    ├── my_report.md
    ├── bibliography.bib
    └── images
```

</div>

<div id="lst:multiple_file_setup" class="listing bash">

Listing 2: Setup with multiple files. Here, `pandoc` would use the
frontmatter of the first document, if available, but I think the
`metadata.yaml` should be provided. This separates configurations from
content in larger projects.

``` bash
├── .devcontainer
├── .vscode
└── docs
    ├── 01_introduction.md
    ├── 02_methodology.md
    ├── 03_conclusion.md
    ├── bibliography.bib
    ├── images
    └── metadata.yaml
```

</div>

When using `academic_markdown`, these situations are distinguished by
the presence of the `metadata.yaml` file. When building a single
document, the situations are barely distinguishable, save for the use of
`metadata.yaml` to provide pandoc with metadata if it is present. When
building a folder, however, the presence of the `metadata.yaml` file
will determine whether a single document or multiple are produced. In
the case a `metadata.yaml` file is found, all the markdown files in the
folder are concatenated into one rendered file. When it is absent, each
document is rendered separately.

#### Quality of Life Improvements - VSCode Extensions and Plugins

I’ve really optimized this workflow for VSCode, which is not to say it
doesn’t work for other IDEs, but it might require some extra
configuration. I do work with NeoVIM from time to time, so I will remark
which plugins I find useful for that too. When using the preconfigured
devcontainer, these will all be installed automatically.

That being said, I have configured the most common actions (building a
single file or a folder with, or without docker) as VSCode tasks. These
are found in the `.vscode/tasks.json` file. VSCode automatically reads
these and can be run by looking up *Run Task* in the command palette. In
NeoVIM, there is a plugin called
[vs-tasks.nvim](https://github.com/EthanJWright/vs-tasks.nvim) (and
several similar others) that will read and execute these tasks
similarly.

While the principle of using markdown is not to get too caught up with
formatting (among others), it is sometimes reassuring to preview your
document, especially if you use intermittent LaTeX for equations. There
are various options, multiple of which are included in the devcontainer.
Firstly, there is the defacto standard [markdown previewer]() which has
incredibly nice interactivity and support for LaTeX equations. Sadly, it
does not support citations (as far as I’m aware). If you’d like
something more akin to the pdf output, there is [Pandoc Renderer]()
which uses `pandoc` to convert the document to HTML. Because it also
uses `pandoc`, it resembles the final PDF ender more closely, which
includes citations and authors defined in the `metadata.yaml`file (if
present). When working in NeoVIM I generally don’t use previews, and so
I do not have plugin ready for that purpose. There seem to be various
such plugins around such as
[`markdown-preview.nvim`](https://github.com/iamcco/markdown-preview.nvim).

Lastly, to be able to effectively use citations, I use the pandoc-citer
to search the bibliography. In case of a single file, it’s easy: just
include the path relative to the current file in the preamble:

<div id="lst:bib_single" class="listing markdown">

Listing 3: How to reference the bibiliography in a standalone markdown
file.

``` markdown
---
title: My Great Work
author: Zohar Cochavi

bibliography: ../work.bib
---

It all started when I was a child...
```

</div>

In case you use the `metadata.yaml` file to define a multi-file
document, my advice is to define the bibliography in the
`.vscode/settings.json` file as indicated in lst. 4.

<div id="lst:bib_mult" class="listing json">

Listing 4: Adding bibliography completion when working with multiple
files.

``` json
{
  "PandocCiter.UseDefaultBib": true,
  "PandocCiter.DefaultBibs": ["work.bib"],
}
```

</div>

I have also included some other extensions such as linters and spelling
checkers. Still, these are the most interesting and worthy of
mentioning. For the full list of included extensions, please check the
`devcontainer.json` configuration file.

#### Other IDEs

## Motivation

My reasoning is as follows: Markdown is a great format to write in but
lacks configurability. LaTeX is great for configurability, but rather
hard to write in (updates take quite a while to render, and the syntax
is sometimes rather distracting). One should focus on writing first, and
then make small adjustments where necessary. For this reason, I first
write in Markdown and then convert to PDF through LaTeX. In case I would
like to customize certain aspects of the exported file, I export to
LaTeX and then to pdf.

While all of this is supported by `pandoc`, finding a system to work
with this is not necessarily trivial. This repository should provide
everything necessary to make the above workflow as smooth as possible
while still allowing for personalization.

## Roadmap

- [x] **Dockerized environment**. Lightweight dockerized environment
  that allows for a full replacement of `pandoc`. Also automatically
  downloads missing latex packages.

- [x] **Devcontainer environment**. Docker container optimized for
  devcontainer (include Microsoft goodies, and reduce Docker image build
  times). And include a range of useful extensions.

- [x] **PyPI Package**. Academic Markdown is now available as a `pypi`
  package! This makes it much easier to install and update the tool.
  Check its progress on
  [academic_markdown_cli](https://www.github.com/cochaviz/academic_markdown_cli)

- [ ] **Full Manual**. A complete and detailed explanation of how this
  workflow can be used. This should be an instruction for any person
  that would like to use markdown for serious writing. It should provide
  an introduction to `pandoc`, docker, and VSCode.

- [ ] **Github Actions for building**. Use GitHub Actions to
  automatically build to PDF, LaTeX according to user preferences. This
  could be useful for ensuring rendered documents are always up-to-date,
  and avoiding the necessity for local builds. Could, perhaps, also be
  faster than building locally and pushing.

- [ ] **Independent VSCode Extension**. A VSCode extension, independent
  of `build.py`. This could be an improved user experience for existing
  VSCode users. This template should, however, still be as usable
  without VSCode.
