from dataclasses import dataclass, field
from typing import List


@dataclass(frozen=True)
class Customer:
    id: str
    name: str
    currency: str = "USD"


@dataclass
class Invoice:
    id: str
    customer_id: str
    amount_cents: int
    paid_cents: int = 0
    currency: str = "USD"

    @property
    def outstanding_cents(self):
        return max(self.amount_cents - self.paid_cents, 0)


@dataclass
class Ledger:
    customers: List[Customer] = field(default_factory=list)
    invoices: List[Invoice] = field(default_factory=list)
