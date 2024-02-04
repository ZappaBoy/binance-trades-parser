# binance-trades-parser

`binance-trades-parser` is a simple parser made to extract show information about PNL from Binance XLSX exported files.

## Installation

This tool uses [poetry](https://python-poetry.org/) to manage dependencies and packaging. To install all the
dependencies
simply run:

``` shell
poetry install
```

## Usage

You can run the tool using poetry:

``` shell
poetry run binance_trades_parser --help
```

Or you can run the tool using python:

``` shell
python -m binance_trades_parser --help
```

Or you can run the tool directly from the directory or add it to your path:

``` shell
isparser --help
```

```shell
usage: binance_trades_parser [-h] [--verbose] [--debug] [--quiet | --no-quiet | -q] [--version] --files FILES [FILES ...] 
```

## Examples
