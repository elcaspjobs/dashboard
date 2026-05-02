import pytest
from uuid import UUID
from src.domain.entities.dashboard import Dashboard
from faker import Faker
import pytest_asyncio

faker = Faker()

SOCIAL_STATS = {
    "youtube": {'viewCount': '22', 'likeCount': '0', 'dislikeCount': '0', 'favoriteCount': '0', 'commentCount': '0'},
    "twitter": {'viewCount': '1242', 'likeCount': '6', 'dislikeCount': '91', 'favoriteCount': '92',
                'commentCount': '93'},
    "instagram": {'viewCount': '531', 'likeCount': '123', 'dislikeCount': '3215', 'favoriteCount': '5235',
                  'commentCount': '2352'},
    "facebook": {'viewCount': '135', 'likeCount': '235', 'dislikeCount': '5235', 'favoriteCount': '235',
                 'commentCount': '1240'},
    "linkedin": {'viewCount': '734', 'likeCount': '98320', 'dislikeCount': '8234', 'favoriteCount': '81234',
                 'commentCount': '8234'},
}


@pytest_asyncio.fixture
async def dashboard_entity():
    data = dashboard_faker()
    return Dashboard(**data)


def dashboard_faker(**overrides):
    social = faker.random_element(elements=SOCIAL_STATS.keys())
    data = {
        "id": faker.uuid4(),
        "social": social,
        "company_id": faker.random_int(min=1, max=100),
        "statistic": SOCIAL_STATS[social],
    }
    data.update(**overrides)
    return data


@pytest.fixture
def dashboard_youtube_entity():
    return Dashboard(
        id=UUID(str(faker.uuid4())),
        social="youtube",
        company_id=faker.random_int(min=1, max=100),
        statistic=SOCIAL_STATS["youtube"],
    )
