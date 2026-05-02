from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any
from uuid import UUID
from sqlalchemy.engine import RowMapping


@dataclass(slots=True)
class Dashboard:
    __hash__ = None
    id: UUID
    social: str
    company_id: int
    statistic: dict[str, Any]

    @classmethod
    def from_orm(cls, dashboard: RowMapping) -> Dashboard:
        return cls(
            id=UUID(str(dashboard.id)),
            social=dashboard.social,
            company_id=dashboard.company_id,
            statistic=dashboard.statistic,
        )

    def __eq__(self, other: Dashboard) -> bool:

        if not isinstance(other, Dashboard):
            return False
        self_dict = asdict(self)
        other_dict = asdict(other)

        self_dict.pop("id", None)
        other_dict.pop("id", None)

        return self_dict == other_dict





