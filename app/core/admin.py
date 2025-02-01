from fastapi_admin.app import app as admin_app
from fastapi_admin.providers.login import UsernamePasswordProvider
from fastapi_admin.models import AbstractAdmin
from fastapi_admin.resources import Field, Model, Action
import aioredis
from app.db.models import User


class Admin(AbstractAdmin):
    pass


async def init_admin():
    redis = await aioredis.create_redis_pool("redis://localhost:6379", encoding="utf-8")

    await admin_app.configure(
        redis=redis,
        logo_url="https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png",
        providers=[
            UsernamePasswordProvider(
                admin_model=Admin,
                login_logo_url="https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png",
            )
        ],
    )


class UserAdmin(Model):
    label = "Usuários"
    model = User
    page_size = 10

    fields = [
        Field(name="id", label="ID"),
        Field(name="username", label="Username"),
        Field(name="email", label="Email"),
    ]

    actions = [
        Action(name="delete", label="Deletar", action="delete", icon="fas fa-trash"),
    ]
