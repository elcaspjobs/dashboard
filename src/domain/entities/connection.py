from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Connection:
    id: int
    social: str
    name: str | None
    account_id: str | None = None
    oauth_token: str | None = None
    access_token: str | None = None
    client_id: str | None = None
    client_secret: str | None = None
    refresh_token: str | None = None
    company_id: int | None = None

    linkedin_org: bool | None = None


@dataclass(frozen=True, slots=True)
class PublishResult:
    connection: Connection
    result_url: str
    company_id: int
