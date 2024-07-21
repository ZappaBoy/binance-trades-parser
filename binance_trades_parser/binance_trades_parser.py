import argparse
import importlib.metadata as metadata
import os
from argparse import Namespace
from statistics import mean
from typing import List

import pandas as pd

from binance_trades_parser.models.log_level import LogLevel
from binance_trades_parser.models.trade import Trade
from binance_trades_parser.models.trade_status import TradeStatus
from binance_trades_parser.shared.utils.logger import Logger

__version__ = metadata.version(__package__ or __name__)

DECIMAL_PLACES = 2


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

            trades: List[Trade] = [Trade.parse_row_object(row.to_dict()) for _, row in df.iterrows()]

            initial_balance = 100
            capital_per_trade = 5
            balance = initial_balance
            portfolio = {}
            profits = []
            for trade in trades:
                if trade.status == TradeStatus.Filled:
                    if trade.pair in portfolio:
                        trade_in_portfolio = portfolio[trade.pair]
                        total_in_portfolio = trade_in_portfolio['total']
                        trade_net_profit = trade.total - total_in_portfolio
                        percentage_profit = trade_net_profit / total_in_portfolio
                        balance += trade_in_portfolio['amount'] * percentage_profit
                        profits.append(percentage_profit)
                        self.logger.info(f'{trade.date} | {trade.pair} {round(percentage_profit * 100, 2)}%')
                        del portfolio[trade.pair]
                    else:
                        if trade.type.is_buy():
                            portfolio[trade.pair] = {
                                'total': trade.total,
                                'amount': balance * capital_per_trade / 100
                            }

            self.logger.info(f'Balance: {round(balance, DECIMAL_PLACES)}')
            self.logger.info(f'Profit: {round((balance - initial_balance) / initial_balance * 100, DECIMAL_PLACES)}%')
            self.logger.info(f'Closed Trades: {len(profits)}')
            self.logger.info(f'Average Profit per Trades: {round(mean(profits) * 100, DECIMAL_PLACES)}%')
            self.logger.info(f'Max profit: {round(max(profits) * 100, DECIMAL_PLACES)}%')
            self.logger.info(f'Max loss: {round(min(profits) * 100, DECIMAL_PLACES)}%')
            self.logger.info(
                f'Accuracy: {round(len([p for p in profits if p > 0]) / len(profits) * 100, DECIMAL_PLACES)}%')
            self.logger.info(
                f'Profit Factor: {round(sum([p for p in profits if p > 0]) / abs(sum([p for p in profits if p < 0])), DECIMAL_PLACES)}')
