from dataclasses import dataclass
from datetime import datetime


@dataclass
class UserSchema:
    user_id: str
    user_balance: float | None
    interaction_sum: float | None
    interaction_type: str | None
    transaction_commission: float | None
    country: str | None
    device: str | None
    date: datetime | None
