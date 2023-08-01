# Appendix

## Syntax Overview

This section is supposed to serve as a reference to the _recommended_ syntax.
In many cases, variations on the syntax exist. I have often chosen not to
include these to ensure clarity and consistency. Especially in the case of
[Figures], the syntax I show is chosen because it operates more easily with
different tools and formats.

### Document Sections

In these examples a multi-document setup is denoted as _MD_, and a
single-document setup as _SD_.

#### Title (MD)

```markdown
title: Title or Section
```

: In a single document, including this in the frontmatter is _not_ the preferred
way of denoting the title, simply for compatibility with other markdown
flavours. In a multi-document setup, this should be denoted in the
`metadata.yaml` file. {#lst:title}

#### Title (SD) or Section (MD)

```markdown
# Title or Section
```

: In single documents, this will be the title. In multi-document formats, this
will denote a level-1 heading or a section. {#lst:title_subsection}

#### Section (SD) or Subsection (MD)

```markdown
## Section (SD) of Subsection (MD)
```

: Section in a single-document setup, or subsection in a multi-document one. {#lst:section_subsection}

#### Subsection (SD) or Subsubsection (MD)

```markdown
### Subsection (SD) or Subsubsection (MD)
```

#### Subsubsection (SD) or Subsubsubsection (MD)

```markdown
#### Subsubsection (SD) or Subsubsubsection (MD)
```

: Subsubsubsubsubsubsubsubsub... {#lst:sub_sub_sub_sub}

### Text formating

Common text is just written as normal text. There are some tricks included in
that might not immediately obvious. To force a newline you can end the current
line with two spaces.  
Line this. A separate paragraph, however, is made by a blank line between two blocks of
text, i.e. two newlines.

The next code blocks show how you can format text in different ways. Like many
other things in markdown, there are multiple syntaxes. These are, however, the
ones that are most commonly used, or simply the type that I consider 'better'
either clarity.

```markdown
Common text
```

_Emphasized text_

```markdown
_Emphasized text_ or *Emphasized text*
```

~~Strikethrough text~~

```markdown
~~Strikethrough text~~
```

**Strong text**

```markdown
__Strong text__ or **Strong text**
```

_**Strong emphasized text**_

```markdown
___Strong emphasized text___ 
or 
***Strong emphasized text***
or
_**Strong emphasized text**_
```

: An alternative is to used the following `***Strong emphasized text***`, but
this is hard to distinguish from normal `**Strong text**` (similarly for
emphasized text). {#lst:strong_emph_alt}

- Bullet list
  - Nested bullet
    - Sub-nested bullet etc
- Bullet list item 2

```markdown
- Bullet list
    - Nested bullet
        - Sub-nested bullet etc
- Bullet list item 2 

-OR-

* Bullet list
    * Nested bullet
        * Sub-nested bullet etc
* Bullet list item 2
```

1. A numbered list
    1. A nested numbered list
    2. Which is numbered
2. Which is numbered

```markdown
1. A numbered list
    1. A nested numbered list
    2. Which is numbered
2. Which is numbered
```

- [ ] An uncompleted task
- [x] A completed task

```markdown
- [ ] An uncompleted task
- [x] A completed task
```

- [ ] An uncompleted task
  - [ ] A subtask

```markdown
- [ ] An uncompleted task
    - [ ] A subtask
```

> Blockquote
>> Nested blockquote

```markdown
> Blockquote
    >> Nested Blockquote
```

### Inter- and Extra-document Links

#### Website Links

[Named Link](https://www.example.com/) or <http://example.com/>

```markdown
[Named Link](https://www.example.com/) or <http://example.com/>
```

Link to [Title (MD)]

```markdown
Link to [Title (MD)]
```

Table, like this one :

First Header | Second Header
-------------|--------------
Content Cell | Content Cell
Content Cell | Content Cell

```markdown
First Header | Second Header
-------------|--------------
Content Cell | Content Cell
Content Cell | Content Cell
```

Adding a pipe `|` in a cell :

First Header | Second Header
-------------|--------------
Content Cell | Content Cell
Content Cell | \|

```markdown
First Header | Second Header
-------------|--------------
Content Cell | Content Cell
Content Cell | \|
```

Left, right and center aligned table

Left aligned Header | Right aligned Header | Center aligned Header
:-------------------|---------------------:|:--------------------:
Content Cell        |         Content Cell |     Content Cell
Content Cell        |         Content Cell |     Content Cell

```markdown
Left aligned Header | Right aligned Header | Center aligned Header
:-------------------|---------------------:|:--------------------:
Content Cell        |         Content Cell |     Content Cell
Content Cell        |         Content Cell |     Content Cell
```

`code()`

```markdown
`code()`
```

```javascript
var specificLanguage_code = 
{
    "data": {
        "lookedUpPlatform": 1,
        "query": "Kasabian+Test+Transmission",
        "lookedUpItem": {
            "name": "Test Transmission",
            "artist": "Kasabian",
            "album": "Kasabian",
            "picture": null,
            "link": "http://open.spotify.com/track/5jhJur5n4fasblLSCOcrTp"
        }
    }
}
```

: An alternative to the backticks is to use three sguiggly lines `~~~`. This is
useful if you want to show a markdown code block in a code block. Not really
useful unless you want tot present markdown notation. {#lst:code_tick_alt}

_Horizontal line :_
- - - -

```markdown
- - - -
```

_Image with alt :_

![picture alt](https://via.placeholder.com/200x150 "Title is optional")

```markdown
![picture alt](http://via.placeholder.com/200x150 "Title is optional")
```

Inline \LaTeX

```latex
$\LaTeX$
```

Block equation:

$$
E = mc^2
$$

```latex
$$
E = mc^2
$$
```

Footnotes:

Something to read for later[^1]

```markdown
Something to read for later[^1]

[^1]: [A Brief History of Time](https://docs.google.com/viewer?a=v&pid=sites&srcid=ZGVmYXVsdGRvbWFpbnxiaW1hbnNpcnBoeXNpY3N8Z3g6NDI1YjFjNzAwZjNjNzc4NA)
```

[^1]: [A Brief History of Time](https://docs.google.com/viewer?a=v&pid=sites&srcid=ZGVmYXVsdGRvbWFpbnxiaW1hbnNpcnBoeXNpY3N8Z3g6NDI1YjFjNzAwZjNjNzc4NA)
