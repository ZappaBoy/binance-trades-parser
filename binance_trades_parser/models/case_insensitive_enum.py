from enum import Enum


class CaseInsensitiveEnum(str, Enum):
    # default_value member is not defined due to the fact that it is not possible to extend an enum if it has already a
    # member
    @classmethod
    def _missing_(cls, value: str):
        # This method allow a case-insensitive enum
        for member in cls:
            if member.lower() == value.lower():
                return member
        # Return Neutral as default value
        return cls.default_value if hasattr(cls, 'default_value') else None

    def __str__(self):
        return self.value
