from dataclasses import dataclass, field


@dataclass
class OfferDTO:
    category: str
    shop: str
    bank: str
    bonus: int
    period: str
    conditions: list[str] = field(default_factory=list)
