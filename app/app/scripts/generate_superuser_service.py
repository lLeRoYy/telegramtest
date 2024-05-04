import random
import string
import enum

from app.repositories.admin_user import RepositoryAdminUser

from loguru import logger


class Answers(enum.Enum):
    yes = "y"
    no = "n"


class SuperUserGenerator:
    """Класс для генерации суперпользователя."""

    def __init__(self, repository_admin_user: RepositoryAdminUser):
        self._repository_admin_user = repository_admin_user

    @staticmethod
    def _get_user_input(prompt, valid_options=None):
        while True:
            user_input = input(prompt)
            if valid_options and user_input not in valid_options:
                logger.info(f"Некорректный ввод: {valid_options}.")
                continue
            return user_input

    @staticmethod
    def _generate_password(length=12):
        characters = string.ascii_letters + string.digits + string.punctuation
        return ''.join(random.choice(characters) for _ in range(length))

    def create_superuser(self):
        self.login = self._get_user_input("Введите логин: ")
        custom_password = self._get_user_input(
            "Хотите ли вы задать свой пароль? (y/n): ", [Answers.yes, Answers.no]
        )
        if custom_password == Answers.yes:
            self.password = self._get_user_input("Введите пароль: ")
        else:
            self.password = self._generate_password()
            logger.info(f"Пароль сгенерирован: {self.password}")

    def save_to_database(self):
        data = {
            "login": self.login,
            "password": self.password,
            "is_active": True,
        }
        self._repository_admin_user.create(obj_in=data, commit=True)
        logger.info("Superuser saved to database successfully.")

    def display_credentials(self):
        logger.info(f"\nСуперпользователь создан!\nLogin: {self.login}\nPassword: {self.password}")
