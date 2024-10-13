from aiogram.types import ReplyKeyboardMarkup,KeyboardButton,InlineKeyboardMarkup,InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from app.database.requests import get_categories,get_category_item


main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Скидки"),KeyboardButton(text="Акции")],
    [KeyboardButton(text="Магазины"),KeyboardButton(text="Вакансии")],
    [KeyboardButton(text="Ассортимент")]
],
    resize_keyboard=True,
    input_field_placeholder="Выберите пункт меню"
)

async def categories():
    all_categories = await get_categories()
    keyboard = InlineKeyboardBuilder()
    for category in all_categories:
        keyboard.add(InlineKeyboardButton(text=category.name, callback_data=f"category_{category.id}"))
    keyboard.add(InlineKeyboardButton(text="Главное меню", callback_data="main_menu"))

    return keyboard.as_markup()


async def items(category_id):
    all_items = await get_category_item(category_id)
    keyboard = InlineKeyboardBuilder()
    for item in all_items:
        keyboard.add(InlineKeyboardButton(text=item.name, callback_data=f"item_{item.id}"))
    keyboard.add(InlineKeyboardButton(text="Главное меню", callback_data="main_menu"))

    return keyboard.as_markup()