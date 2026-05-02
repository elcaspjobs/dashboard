import uuid

import pytest
from src.application.interactors.dashboard_interactor import DashboardInteractor
from unittest.mock import patch, AsyncMock
from src.domain.entities.dashboard import Dashboard


@patch("src.application.interactors.dashboard_interactor.SocialFactory.create")
@pytest.mark.asyncio
async def test_dashboard_interactor(mock_create, logger, insert_publication, http_service, uow):
    logger.info("Тест интерактора дашборда")
    await insert_publication()

    mock_social_instance = AsyncMock()
    mock_social_instance.get_statistic.return_value = Dashboard(
        id=uuid.uuid4(),
        social="youtube",
        company_id=1,
        statistic={
            'viewCount': '0',
            'likeCount': '0',
            'dislikeCount': '0',
            'favoriteCount': '0',
            'commentCount': '0'
        }
    )

    mock_create.return_value = mock_social_instance

    dashboard_interactor = DashboardInteractor(
        logger=logger,
        http_service=http_service,
        uow=uow,
    )

    await dashboard_interactor()

    mock_create.assert_called()
    mock_social_instance.get_statistic.assert_awaited_once()

