from app.models.mixins import AbstractAdminUser, UUIDMixin
from app.db.base import Base

from flask_login import UserMixin


class AdminUser(AbstractAdminUser, UUIDMixin, UserMixin, Base):
    """Модель пользователя для административной панели"""

    __tablename__ = 'admin_user'

    def __repr__(self) -> str:
        return f"Пользователь: {self.id} | {self.login}"
