from dependency_injector import containers, providers

from app.core.config import Settings
from app.db.session import SyncSession

from app.repositories.telegram_user import RepositoryTelegramUser
from app.repositories.admin_user import RepositoryAdminUser

from app.models.telegram_user import TelegramUser
from app.models.admin_user import AdminUser

from app.services.telegram_user_service import TelegramUserService


class Container(containers.DeclarativeContainer):

    config = providers.Singleton(Settings)
    db = providers.Singleton(SyncSession, db_url=config.provided.postgres_url)
    session = providers.Factory(db().create_session)

    # region repository
    repository_telegram_user = providers.Singleton(
        RepositoryTelegramUser, model=TelegramUser, session=session
    )
    repository_admin_user = providers.Singleton(
        RepositoryAdminUser, model=AdminUser, session=session
    )
    # endregion

    # region services
    telegram_user_service = providers.Singleton(
        TelegramUserService, repository_telegram_user=repository_telegram_user
    )
    # endregion
