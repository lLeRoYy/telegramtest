from flask_admin.contrib.sqla import ModelView
from flask_login import current_user


class CustomModelView(ModelView):

    async def is_accessible(self):
        user = await current_user
        return user.is_authenticated
