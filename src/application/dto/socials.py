from dataclasses import dataclass, asdict


@dataclass(frozen=True, slots=True)
class YoutubeDTO:
    access_token: str
    client_id: str
    client_secret: str
    refresh_token: str
    video_id: str

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class LinkedinDTO:
    post_id: str
    token: str
    account_id: str | None = None

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class TwitterDTO:
    twitter_url: str
    api_bright_token: str
    dataset_twitter: str

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class InstagramDTO:
    post_id: str
    access_token: str
    user_id: str

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class FacebookDTO:
    post_id: str
    access_token: str
    user_id: str

    def to_dict(self) -> dict:
        return asdict(self)
