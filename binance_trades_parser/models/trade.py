from datetime import date, datetime
from typing import Optional

from pydantic.v1 import validator

from binance_trades_parser.models.custom_base_model import CustomBaseModel
from models.side import Side
from models.trade_status import TradeStatus


class Trade(CustomBaseModel):
    date: date
    order_number: int
    pair: str
    type: Side
    order_price: float
    order_amount: float
    average_price: float
    filled: float
    total: float
    trigger_condition: Optional[str]
    status: TradeStatus

    @validator("date", pre=True)
    def parse_birthdate(cls, value):
        return datetime.strptime(
            value,
            "%Y-%m-%d %H:%M:%S"
        ).date()

    @staticmethod
    def parse_row_object(row: dict):
        return Trade.parse_obj({
            'date': datetime.strptime(row['Date(UTC)'], "%Y-%m-%d %H:%M:%S").date(),
            'order_number': row['OrderNo'],
            'pair': row['Pair'],
            'type': row['Type'],
            'order_price': row['Order Price'],
            'order_amount': row['Order Amount'],
            'average_price': row['AvgTrading Price'],
            'filled': row['Filled'],
            'total': row['Total'],
            'trigger_condition': row['Trigger Condition'],
            'status': row['status']
        })
