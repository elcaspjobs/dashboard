import pytest
from src.infrastructure.connections.social_factory import SocialFactory
from src.infrastructure.connections.youtube import Youtube
from src.infrastructure.connections.linkedin import Linkedin


@pytest.mark.asyncio
async def test_social_factory():
    assert SocialFactory._registry["linkedin"] is Linkedin
    assert SocialFactory._registry["youtube"] is Youtube

    assert "linkedin" in SocialFactory._registry
    assert "youtube" in SocialFactory._registry


@pytest.mark.asyncio
async def test_create_social_factory(http_service, insert_connection):
    connection = await insert_connection()

    social = SocialFactory.create(
        http_service=http_service,
        connection=connection,
        social="linkedin"
    )
    assert isinstance(social, Linkedin)
    assert social.connection == connection
