from app.database.models import async_session
from app.database.models import User, Category, Item
from sqlalchemy import select

async def set_user(tg_id: int)-> None:
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            session.add(User(tg_id=tg_id))
            await session.commit()


async def get_categories() :
    async with async_session() as session:
        return await session.scalar(select(Category))

async def get_category_item(category_id):
    async with async_session() as session:
        return await session.scalar(select(Item).where(Item.category == category_id))

async def get_discounted_items():
    async with async_session() as session:
        result = await session.scalars(select(Item).where(Item.discount > 0))
        return result.all()

async def get_category_id_by_name(category_name: str):
    async with async_session() as session:
        result = await session.scalar(select(Category.id).where(Category.name == category_name))
        return result

async def get_discounted_items_by_category(category_id: int):
    async with async_session() as session:
        result = await session.scalars(select(Item).where(Item.category == category_id).where(Item.discount > 0))
        return result.all()  # Возвращаем все товары со скидками