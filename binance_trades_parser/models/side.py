from models.case_insensitive_enum import CaseInsensitiveEnum


class Side(CaseInsensitiveEnum):
    Buy = 'Buy'
    Sell = 'Sell'
    Neutral = 'Neutral'
    default_value = Neutral

    def is_sell(self):
        return self == Side.Sell

    def is_buy(self):
        return self == Side.Buy

    def is_neutral(self):
        return self == Side.Neutral
