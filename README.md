# Academic Markdown - Tools and Guide

This repository contains my workflow for using markdown and pandoc for academic
writing and serves as a template for that workflow. If you're just looking to
try it out, press the green button that says _Use This Template_ and open in a
code space.  Otherwise, continue reading to set up a more permanent version of
this environment.

In this README, you will find instructions on how to use `build.py` and the
provided `Dockerfile`. That is, how to set up your system to successfully build
markdown files to `pdf`, $\LaTeX$, `HTML`, and markdown (that is
Github-flavoured markdown with rendered citations).

In _Workflow_, I will show how I work with these tools.

## Quickstart

To start, you can choose to:

- [Use the provided
Dockerfile](https://www.docker.com/) to set up a Docker container

- Install the
required dependencies ([`pandoc`](https://pandoc.org/),
[`pandoc-crossref`](https://github.com/lierdakil/pandoc-crossref), and
[$\LaTeX$](https://www.latex-project.or/)) yourself

- Open this template in a
Github code-space (green button in the top-right of the repository)

- [Open
locally in a VSCode
devcontainer](https://vscode.dev/redirect?url=vscode://ms-vscode-remote.remote-containers/cloneInVolume?url=https://github.com/cochaviz/academic_markdown).

If you are on Github, using codespaces is definitely the easiest if you'd just
like to have a look around.

## Capabilities

For my writing, I wanted to be able to do the following things:

- Citations with `.bib`
- Figures with captions
- Export to $\LaTeX$, `markdown`, `HTML`
- Use common journal $\LaTeX$ templates
