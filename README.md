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

To start, you can choose to use the provided Dockerfile to set up a Docker
container, install the required dependencies (`pandoc`, `pandoc-crossref`, and
$\LaTeX$) yourself, or open this template in a Github code-space.

[![Open in Dev Containers](https://img.shields.io/static/v1?label=Dev%20Containers&message=Open&color=blue&logo=visualstudiocode)](https://vscode.dev/redirect?url=vscode://ms-vscode-remote.remote-containers/cloneInVolume?url=https://github.com/cochaviz/academic_markdown)

## Capabilities

For my writing, I wanted to be able to do the following things:

- Citations with `.bib`
- Figures with captions
- Export to $\LaTeX$, `markdown`, `HTML`
- Use common journal $\LaTeX$ templates
