from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Any
from datetime import datetime, timezone
from uuid import UUID
from sqlalchemy.engine import RowMapping


@dataclass(slots=True)
class Dashboard:
    __hash__ = None
    id: UUID
    social: str
    company_id: int
    stats_kwargs: dict[str, Any]
    created_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc).replace(tzinfo=None)
    )

    @classmethod
    def from_orm(cls, dashboard: RowMapping) -> Dashboard:
        return cls(
            id=UUID(str(dashboard.id)),
            social=dashboard.social,
            company_id=dashboard.company_id,
            stats_kwargs=dashboard.stats_kwargs,
            created_at=dashboard.created_at,
        )

    def __eq__(self, other: Dashboard) -> bool:

        if not isinstance(other, Dashboard):
            return False
        self_dict = asdict(self)
        other_dict = asdict(other)

        self_dict.pop("id", None)
        other_dict.pop("id", None)

        return self_dict == other_dict





