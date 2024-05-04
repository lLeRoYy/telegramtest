from flask import Flask, render_template, request, redirect
from flask_admin import Admin
from flask_login import LoginManager, login_user
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy import select

from app.db.session import ASyncSession, ASyncSession
from app.core.config import settings

from app.admin.views.tg_user import TelegramUserView

from app.models.telegram_user import TelegramUser
from app.models.admin_user import AdminUser

from loguru import logger

session = ASyncSession(db_url=settings.postgres_url)

secureApp = Flask(__name__)
login = LoginManager(secureApp)


@login.user_loader
async def load_user(user_id):
    session_factory: AsyncSession = session.create_session()
    stmt = select(AdminUser).filter_by(id=user_id)
    resul = await session_factory.execute(stmt)
    return resul.scalar_one()


secureApp.config["SECRET_KEY"] = settings.secret_key


class Middleware:
    """Simple WSGI middleware"""

    def __init__(self, app, session_factory):
        self.app = app
        self.session_factory = session_factory

    async def __call__(self, environ, start_response):
        session: AsyncSession = self.session_factory()
        try:
            return self.app(environ, start_response)
        except Exception as exc:
            print(exc)
            await session.rollback()
        finally:
            session.expunge_all()
            await session.close()


Middleware(secureApp.wsgi_app, session_factory=session.session)

# create administrator
admin = Admin(
    secureApp, name="Admin", base_template="my_master.html", template_mode="bootstrap4"
)
# Add view
# error get_event_loop, async_session
admin.add_view(TelegramUserView(TelegramUser, session))


@secureApp.route("/admin/login/", methods=["POST", "GET"])
async def login():
    async_session = session.create_session()
    if request.method == "POST":
        users_login = request.form.get("login")
        password = request.form.get("password")
        stmt = select(AdminUser).filter_by(password=password, login=users_login)
        resul = await async_session.execute(stmt)
        user = resul.scalar_one()
        if user.is_active:
            logger.info("go to login")
            login_user(user)
        return redirect("/admin")
    else:
        return render_template("index.html")
