import argparse
import importlib.metadata as metadata
import os
from argparse import Namespace
from typing import List

import pandas as pd

from models.log_level import LogLevel
from models.trade import Trade
from shared.utils.logger import Logger

__version__ = metadata.version(__package__ or __name__)


class BinanceTradesParser:
    def __init__(self):
        self.logger = Logger()
        self.args = self.parse_args()
        self.set_verbosity()

    def run(self):
        self.check_args()
        self.logger.info(f"Running...")
        self.logger.debug(self.args)
        for file in self.args.files:
            self.logger.info(f"Processing file: {file}")
        self.parse(files=self.args.files)

    @staticmethod
    def parse_args() -> Namespace:
        parser = argparse.ArgumentParser(
            description="binance_trades_parser is a simple tool to parse and simply show the portfolio profitability "
                        "from Binance XLSX trade files.")
        parser.add_argument('--verbose', '-v', action='count', default=1,
                            help='Increase verbosity. Use more than once to increase verbosity level (e.g. -vvv).')
        parser.add_argument('--debug', action='store_true', default=False,
                            help='Enable debug mode.')
        parser.add_argument('--quiet', '-q', action=argparse.BooleanOptionalAction, default=False,
                            required=False, help='Do not print any output/log')
        parser.add_argument('--version', action='version', version=f'%(prog)s {__version__}',
                            help='Show version and exit.')
        parser.add_argument('--files', '-f', required=True, action='store',
                            nargs='+', help='Trades XLSX file(s) to use')
        return parser.parse_args()

    def check_args(self) -> None:
        error_message = ""
        for file in self.args.files:
            if not os.path.exists(file):
                error_message += f"\nIncorrect input file: {file}"
        if error_message != "":
            self.logger.error(error_message)
            exit(1)

    def set_verbosity(self) -> None:
        if self.args.quiet:
            verbosity_level = LogLevel.DISABLED
        else:
            if self.args.debug or self.args.verbose > LogLevel.DEBUG.value:
                verbosity_level = LogLevel.DEBUG
            else:
                verbosity_level = self.args.verbose
        self.logger.set_log_level(verbosity_level)

    def parse(self, files: List[str]) -> None:
        for filename in files:
            self.logger.info(filename)

            index_column_name = "Date(UTC)"
            df = pd.read_excel(filename, engine="openpyxl", dtype={
                'Date(UTC)': 'string',
                'OrderNo': 'int64',
                'Pair': 'string',
                'Type': 'string',
                'Order Price': 'float64',
                'Order Amount': 'float64',
                'AvgTrading Price': 'float64',
                'Filled': 'float64',
                'Total': 'float64',
                'Trigger Condition': 'string',
                'status': 'string',
            })
            df = df.sort_values(by=index_column_name)

            for index, row in df.iterrows():
                trade = Trade.parse_row_object(row.to_dict())
                print(trade)
