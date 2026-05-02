import pytest
from src.domain.entities.connection import PublishResult

import datetime


@pytest.mark.asyncio
async def test_publication_repo(uow, insert_publication, logger):
    logger.info("TEST PUBLICATION GET REPO")
    pub1 = await insert_publication()
    pub2 = await insert_publication()
    pub3 = await insert_publication()
    publish_time = datetime.datetime.now() - datetime.timedelta(hours=5)

    pub4 = await insert_publication(publish_time=publish_time)

    logger.info(f"Publication: {pub1} \n pub 2{pub2} pub3\n {pub3} pub4\n {pub4}")

    result = await uow.publication.filter_by_time()
    await uow.commit()

    logger.info(f"results: {result}")

    assert isinstance(result, list)
    assert len(result) == 4
    assert all(isinstance(r, PublishResult) for r in result)
