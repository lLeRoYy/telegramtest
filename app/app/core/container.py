from dependency_injector import containers, providers

from app.core.config import Settings
from app.db.session import SyncSession

from app.repositories.telegram_user import RepositoryTelegramUser
from app.repositories.admin_user import RepositoryAdminUser

from app.models.telegram_user import TelegramUser
from app.models.admin_user import AdminUser

from app.scripts.generate_superuser_service import SuperUserGenerator


class Container(containers.DeclarativeContainer):

    config = providers.Singleton(Settings)
    db = providers.Singleton(SyncSession, db_url=str(config.provided.postgres_url))

    # region repository
    repository_telegram_user = providers.Singleton(RepositoryTelegramUser, model=TelegramUser, session=db)
    repository_admin_user = providers.Singleton(RepositoryAdminUser, model=AdminUser, session=db)
    # endregion

    # region service
    create_super_user_service = providers.Singleton(SuperUserGenerator, repository_admin_user=repository_admin_user)
    # endregion
