# Conventions - Using Markdown

The goal of writing in Markdown is to use a minimal set of markup options,
thereby maintaining focus on writing instead of formatting. Of course, this
limits the number of options when wanting to format your document, but the first
step should really be to write.

The problem is that quite a few Markdown definitions exist. Originally, it was
meant for converting to HTML, but many have adopted it to work for a range of
formats to export to.

## A Brief History

## Our Convention

Considering the context in which the original markdown spec was created, we have
some special requirements that should be accommodated with extended syntax. In
an academic context, large complex documents are the norm and special attention
should therefore be given to the use of (i) figures and internal references,
and (ii) external references.

### Figures and Internal References

Firstly, figures and internal references provide structure and clarity within a
document. There should not be any contention concerning the figure, table, or
resource that is referenced. When writing in LaTeX, for example, a figure is
simply denoted by `\begin{figure}` and the corresponding caption number is
automatically generated, and links are created by internal `\label` and `\ref`
commands. This avoids the need for constant updating of figure numbers, markup we
would not want to bother ourselves with when writing.

As the original Markdown spec required a minimal markup syntax, this was
omitted. Such functionality could still be accessed through the use of anchor
`<a>` tags. But since we would like complete interoperability between LaTeX and
Markdown, we need something more native.

Thus, to accommodate the use of figures, and especially figure captions and
references, we use `pandoc-crossref`. This `pandoc` filter[^pandoc_filter]
extends the Markdown syntax to include figure markup and automatically generates
link identifiers for headers/sections too (see [Figures] for examples). This one
of the great things about `pandoc`, as it is very configurable it can be molded
to your specific needs. But this of course has a downside, namely that it can be
quite complex.

Since we are working in `pandoc` and it allows for some extensions which are not
native to Markdown, it is important to note that we work in _pandoc-flavored_
Markdown. Including this style of Markdown in for example Github READMEs, might
give mixed results depending on the features used. This is not necessarily a
problem as you will simply realize that GitHub does not support a particular
feature (figures are one such example), but it is important to realize Markdown
is not fully standardized and be aware of such issues. Therefore, we export from
our pandoc-flavored Markdown to _GitHub-flavored_ Markdown with `pandoc`[^github_flavored_markdown].

[^pandoc_filter]: A `pandoc` filter is a program that is run in series with the
    parser (in this case the Markdown parser). In this case, the filter is used to
    extend the Markdown syntax, but it can be used for various other purposes as
    well.

[^github_flavored_markdown]: In `pandoc`, GitHub-flavored Markdown is denoted as
    `gfm`. When exporting to Markdown with `academic-markdown.py`, this is the
    default setting.

### External References or Citations
