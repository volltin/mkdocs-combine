# Description

This module combines a
[MkDocs](http://www.mkdocs.org)-style Markdown source site into a single Markdown document, which can optionally be
[pandoc](http://www.pandoc.org)-flavoured. This is useful
for

* Generating PDF or EPUB from your MkDocs documentation
* Generating single-page HTML from your MkDocs documentation
* Converting your MkDocs documentation to other formats, such as asciidoc.

Aside from the filters the module contains a converter class tying them
together into a coherent whole, and the command line converter `mkdocscombine`.

# Prerequisites

For generating PDF through pandoc you will need to install a few things
pip won't handle, namely pandoc and the somewhat exotic LaTeX packages its
default LaTeX template uses. On a Ubuntu 14.04 system this amounts to the
following packages:

```
fonts-lmodern
lmodern
pandoc
texlive-base
texlive-latex-extra
texlive-fonts-recommended
texlive-latex-recommended
texlive-xetex
```
On a Windows system you can get them through
[Chocolatey](https://chocolatey.org/). Once you have Chocolatey up and running
the following commands should leave you with everything you need to create PDF
output from Pandoc:

```
choco install python
choco install pandocpdf
```

# Installation

_Note: The following instructions apply to both Unixoid systems and Windows._

If you'd like to use the development version, use

```
pip install git+https://github.com/twardoch/mkdocs-combine
```

instead. Note that if you are behind a proxy, you might need to add the `--proxy` option like this

```
pip --proxy=http[s]://user@mydomain:port install ...
```

# Usage

When executed in the directory where your documentation's `mkdoc.yml` and the
`docs/` directory containing the actual documentation resides, `mkdocscombine`
should print one long Markdown document suitable for `pandoc(1)` on standard
output. This works under the following assumptions:

## Usage example

```
cd ~/mydocs
mkdocscombine -o mydocs.pd
pandoc --toc -f markdown+grid_tables+table_captions -o mydocs.pdf mydocs.pd   # Generate PDF
pandoc --toc -f markdown+grid_tables -t epub -o mydocs.epub mydocs.pd         # Generate EPUB
```

# Bugs

The following things are known to be broken:

Line wrapping in table cells will wrap links, which causes
Line wrapping in table cells will wrap links, which causes
  whitespace to be inserted in their target URLs, at least in PDF output. While
  this is a bit of a Pandoc problem, it can and should be fixed in this module.

* [Internal Hyperlinks](http://www.mkdocs.org/user-guide/writing-your-docs/#internal-hyperlinks) 
  between markdown documents will be reduced to their link titles, i.e. they
  will not be links in the resulting Pandoc document.

# Copyright

(C) 2015 Johannes Grassler <johannes@btw23.de>
(C) 2017 Adam Twardoch <adam+github@twardoch.com>

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

You will also find a copy of the License in the file `LICENSE` in the top level
directory of this source code repository. In case the above URL is unreachable
and/or differs from the copy in this file, the file takes precedence.

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
