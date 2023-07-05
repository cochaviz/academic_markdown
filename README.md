# Academic Markdown - Tools and Guide

This repository contains my workflow for using markdown and pandoc for academic
writing and serves as a template for that workflow. To get started with writing,
press the green button that says _Use This Template_, and continue reading the
instructions.

In this README, you will find instructions on how to use `build.py` and the
provided `Dockerfile`. That is, how to set up your system to successfully build
markdown files to `pdf`, $\LaTeX$, `HTML`, and markdown (that is
Github-flavoured markdown with rendered citations).

In _Workflow_, I will show how I work with these tools.

## Quickstart

To start, you can choose to [use the provided
Dockerfile](https://www.docker.com/) to set up a Docker container, install the
required dependencies ([`pandoc`](https://pandoc.org/),
[`pandoc-crossref`](https://github.com/lierdakil/pandoc-crossref), and
[$\LaTeX$](https://www.latex-project.org/)) yourself, open this template in a
Github code-space (green button in the top-right of the repository), or [open
locally in a VSCode
dev-container](https://vscode.dev/redirect?url=vscode://ms-vscode-remote.remote-containers/cloneInVolume?url=https://github.com/cochaviz/academic_markdown).

## Capabilities

For my writing, I wanted to be able to do the following things:

- Citations with `.bib`
- Figures with captions
- Export to $\LaTeX$, `markdown`, `HTML`
- Use common journal $\LaTeX$ templates
