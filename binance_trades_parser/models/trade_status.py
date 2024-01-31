from models.case_insensitive_enum import CaseInsensitiveEnum


class TradeStatus(CaseInsensitiveEnum):
    Filled = 'Filled'
    default_value = Filled
