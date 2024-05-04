from dependency_injector.wiring import inject, Provide

from app.core.container import Container
from loguru import logger


@inject
def create_super_user(create_super_user_service=Provide[Container.create_super_user_service]) -> None:
    logger.info(create_super_user_service)
    create_super_user_service.create_superuser()
    create_super_user_service.save_to_database()
    create_super_user_service.display_credentials()


if __name__ == "__main__":
    create_super_user()
