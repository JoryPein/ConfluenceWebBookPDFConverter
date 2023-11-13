# Confluence Web Book to PDF Converter

This tool allows you to generate a PDF from a Confluence web book. 

Follow the steps below to use the converter.

## Prerequisites

Make sure you have Python 3.7 installed on your system. If not, you can download it from [Python's official website](https://www.python.org/downloads/release).

## Installation

Use the following commands to install the required dependencies:

```bash
python3.7 -m pip install -r requirements.txt
```

## Usage

1. Run the script to download the Confluence web book:

```bash
python3.7 down-link.py
```

2. Build the PDF from the downloaded content:

```bash
python3.7 build-pdf.py
```

The generated PDF will be available in the output directory.
