#!/usr/bin/python
#
# Copyright 2015 Johannes Grassler <johannes@btw23.de>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# mkdocscombine - combines an MkDocs source site into a single Markdown document

from __future__ import print_function

import argparse
import codecs
import sys

import mkdocs_combine
from mkdocs_combine.exceptions import FatalError

__version__ = '0.3.0.0'

def main():
    opts = argparse.ArgumentParser(
        description="mkdocscombine.py " +
                    "- combines an MkDocs source site into a single Markdown document")

    opts.add_argument('-v', '--version', action='version',
                      version='%(prog)s {version}'.format(version=__version__))

    opts_files = opts.add_argument_group('Files')
    opts_files.add_argument('-o', '--outfile', default=None,
                            help="Write combined Markdown document to path (default: STDOUT)")
    opts_files.add_argument('-e', '--encoding', default='utf-8',
                            help="Set encoding for input files (default: utf-8)")
    opts_files.add_argument('-x', '--exclude', default=None, action='append',
                            help="Exclude Markdown files from processing (default: none)")

    opts_mkdocs = opts.add_argument_group('MkDocs')
    opts_mkdocs.add_argument('-f', '--config-file', default='mkdocs.yml',
                             help="MkDocs configuration file to use")

    opts_meta = opts.add_argument_group('Metadata')
    opts_strip_metadata = opts_meta.add_mutually_exclusive_group(required=False)
    opts_strip_metadata.add_argument('-m', '--meta', dest='strip_metadata', action='store_false',
                                     help='Keep YAML metadata (default)')
    opts_strip_metadata.add_argument('-M', '--no-meta', dest='strip_metadata', action='store_true',
                                     help='Strip YAML metadata'))
    opts.set_defaults(strip_metadata=False)

    opts_add_chapter_heads = opts_meta.add_mutually_exclusive_group(required=False)
    opts_add_chapter_heads.add_argument('-t', '--titles', dest='add_chapter_heads', action='store_true',
                                    help = 'Add chapter titles from mkdocs.yml to chapter files (default)')
    opts_add_chapter_heads.add_argument('-T', '--no-titles', dest='add_chapter_heads', action='store_false',
                                    help = 'Do not add chapter titles'))
    opts.set_defaults(add_chapter_heads=True)

    opts_tables = opts.add_argument_group('Tables')
    opts_filter_tables = opts_tables.add_mutually_exclusive_group(required=False)
    opts_filter_tables.add_argument('-g', '--grid-tables', dest='filter_tables', action='store_true',
                                    help='Convert Markdown tables to Pandoc-style grid tables'))
    opts_filter_tables.add_argument('-G', '--orig-tables', dest='filter_tables', action='store_false',
                                    help='Keep original Markdown tables')
    opts.set_defaults(filter_tables=False)

    opts_tables.add_argument('-w', '--width', default=100,
                             help="Width of generated grid tables in characters (default: 100)")

    opts_links = opts.add_argument_group('Links')
    opts_filter_xrefs = opts_links.add_mutually_exclusive_group(required=False)
    opts_filter_xrefs.add_argument('-r', '--xrefs', dest='filter_xrefs', action='store_false',
                                   help='Keep MkDocs-style cross-references'))
    opts_filter_xrefs.add_argument('-R', '--no-xrefs', dest='filter_xrefs', action='store_true',
                                   help='Replace MkDocs-style cross-references by just their title (default)')
    opts.set_defaults(filter_xrefs=True)

    opts_strip_anchors = opts_links.add_mutually_exclusive_group(required=False)
    opts_strip_anchors.add_argument('-a', '--anchors', dest='strip_anchors', action='store_false',
                                    help='Keep HTML anchor tags')
    opts_strip_anchors.add_argument('-A', '--no-anchors', dest='strip_anchors', action='store_true',
                                    help='Strip out HTML anchor tags (default)')
    opts.set_defaults(strip_anchors=True)

    opts_extras = opts.add_argument_group('Extras')
    opts_convert_math = opts_extras.add_mutually_exclusive_group(required=False)
    opts_convert_math.add_argument('--convert-math', dest='convert_math', action='store_true',
                                   help='Turn the \( \) Markdown math notation into LaTex $$ inlines')
    opts_convert_math.add_argument('--no-convert-math', dest='convert_math', action='store_false',
                                   help='Keep \( \) Markdown math notation (default)'))
    opts.set_defaults(convert_math=False)

    opts_extras.add_argument('-i', '--image-ext', default=None,
                             help="Substitute image extensions by (default: no replacement)")

    args = opts.parse_args()

    # Python 2 and Python 3 have mutually incompatible approaches to writing
    # encoded data to sys.stdout, so we'll have to pick the appropriate one.

    if sys.version_info.major == 2:
        out = codecs.getwriter(args.encoding)(sys.stdout)
    elif sys.version_info.major >= 3:
        out = open(sys.stdout.fileno(), mode='w', encoding=args.encoding, buffering=1)


try:
    pconv = mkdocs_combine.MkDocsCombiner(
        config_file=args.config_file,
        exclude=args.exclude,
        image_ext=args.image_ext,
        width=args.width,
        encoding=args.encoding,
        filter_tables=args.filter_tables,
        filter_xrefs=args.filter_xrefs,
        strip_anchors=args.strip_anchors,
        strip_metadata=args.strip_metadata,
        convert_math=args.convert_math,
        add_chapter_heads=args.add_chapter_heads,
    )
except FatalError as e:
    print(e.message, file=sys.stderr)
    return (e.status)
if args.outfile:
    try:
        out = codecs.open(args.outfile, 'w', encoding=args.encoding)
    except IOError as e:
        print("Couldn't open %s for writing: %s" % (args.outfile, e.strerror), file=sys.stderr)

for line in pconv.convert():
    out.write(line + '\n')
out.close()
