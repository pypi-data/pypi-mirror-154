[![Build Status](https://drone.chaoslama.org/api/badges/EorlBruder/make_pdf/status.svg)](https://drone.chaoslama.org/EorlBruder/make_pdf) [![PyPI version](https://badge.fury.io/py/make_pdf.svg)](https://badge.fury.io/py/make_pdf)

A command line tool to convert files to fancy PDFs.

This tool generates nice-looking reports, letters, presentations etc. from Markdown. Other formats also work, but aren't really supported. The only Output format is PDF.

You can use custom themes with customizable fonts, logos and names. 

# Installation

You can install this tool by running `pip install make_pdf`.

## Requirements

This project requires python (at leas 3.6) and pip. 

Furthermore, texlive and a bunch of packages for it need to be installed. Here I opted for just installing [texlive-most](https://archlinux.org/groups/x86_64/texlive-most/) on Arch Linux.

If you're running this on Linux you may need to install [pandoc](https://pandoc.org/).

Furthermore, you need the following fonts: Roboto, Inconsolata and Yanone Kaffeesatz installed.

## From source

You can also build it from source yourself.

1. Clone this repository: `git clone https://git.eorlbruder.de/EorlBruder/mdp2df.git`
3. Install with pip: `pip install .`

# Usage

By default, this tool only requires an input-file. Thus, the following command works as a minimal example:

```bash
make_pdf plain test.md
```

This command will create a `test-plain.pdf`-file. You can also provide multiple input-files `make_pdf plain test.md test1.md`.

All input-file-types supported by [pandoc](https://pandoc.org/) are supported, but some features will only work with markdown.

You'll get a bunch more information with `make_pdf --help` or using the `--help` flag after any command.

You'll also find much more information in the [docs](https://make-pdf.de/).

## Commands

Make_pdf has four commands for generating files. 

The first one you already know, it's `plain`. This generates a simple document, like for example a report or a handout.

Then there's `newsletter`. This is very similar to plain - only that every section gets displayed in a box, as well as the title. 

Next we have `letter`. This command needs some extra metadata and generates a formal letter. 

Last but not least there's `presentation` which generates a beamer-presentation.

Every command will generate a file with the name of the mode as its suffix, so for example `make_pdf letter test.md` generates `test-letter.pdf`.

## Options

You can provide every command with options. You can find out which ones are available in particular by using `make_pdf <command> --help`.

## Metadata

Files generally get generated with their metadata. You have several options to provide them.

First, if you're using Markdown you can provide the title, author and date at the beginning of the file:

```markdown
% Title
% Author
% Date
```

You can also provide them in a yaml-block:

```markdown
---
title: Title
author: Author
date: Date
---
```

You can also provide them via a separate yml-file, which you just provide together with the input-files:

```bash
make_pdf plain metadata.yml file.md
```

Last, there's also the option to provide them as options:

```bash
make_pdf plain file.md --title Title --author Author --date Date
```

If you don't provide a date, it will be automatically set to today's date. If you don't want this behaviour, you can disable it with the `--no-automatic-date`-option.


# Contribute

To see how to contribute please have a look at the CONTRIBUTING.md-file.
