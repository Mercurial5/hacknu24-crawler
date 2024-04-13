from dataclasses import dataclass, field


@dataclass
class OfferDTO:
    category: str
    shop: str
    bank: str
    bonus: int
    conditions: list[str] = field(default_factory=list)
