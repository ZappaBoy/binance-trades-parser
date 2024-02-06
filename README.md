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
`binance_trades_parser --help`
```

```shell
usage: binance_trades_parser [-h] [--verbose] [--debug] [--quiet | --no-quiet | -q] [--version] --files FILES [FILES ...]

binance_trades_parser is a simple tool to parse and simply show the portfolio profitability from Binance XLSX trade files.

options:
  -h, --help            show this help message and exit
  --verbose, -v         Increase verbosity. Use more than once to increase verbosity level (e.g. -vvv).
  --debug               Enable debug mode.
  --quiet, --no-quiet, -q
                        Do not print any output/log
  --version             Show version and exit.
  --files FILES [FILES ...], -f FILES [FILES ...]
                        Trades XLSX file(s) to use
 
```

## Examples
