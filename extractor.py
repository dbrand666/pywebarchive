#!/usr/bin/env python3

"""Simple command-line .webarchive extractor."""

import os
import sys
import optparse
import webbrowser

import webarchive


def main():
    """Extract the .webarchive file specified on the command line."""

    parser = optparse.OptionParser(
        usage="%prog [options] input_path.webarchive [output_path.html]"
    )

    opt_group = parser.add_option_group("Extraction mode")
    opt_group.add_option("-s", "--single-file",
                         action="store_true", dest="single_file",
                         help="extract archive contents to a single HTML file "
                              "with embedded resources (experimental)")

    opt_group = parser.add_option_group("Post-processing actions")
    opt_group.add_option("-o", "--open-page",
                         action="store_true", dest="open_page",
                         help="open the extracted webpage when finished")

    options, args = parser.parse_args()
    if len(args) == 1:
        # Get the archive path from the command line
        archive_path = args[0]

        # Derive the output path from the archive path
        base, ext = os.path.splitext(archive_path)
        output_path = "{0}.html".format(base)

    elif len(args) == 2:
        # Get the archive and output paths from the command line
        archive_path, output_path = args

    else:
        # Print the correct usage and exit
        parser.print_usage(file=sys.stderr)
        sys.exit(1)

    # Extract the archive
    archive = webarchive.open(archive_path)
    archive.extract(output_path,
                    single_file=options.single_file)

    if options.open_page:
        # Open the extracted page
        webbrowser.open(output_path)


if __name__ == "__main__":
    main()
