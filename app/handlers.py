from aiogram import F, Router, types
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, CallbackQuery, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.utils.keyboard import InlineKeyboardBuilder
import logging


import app.keyboards as kb
import app.database.requests as rq
from app.database.models import async_session, Item

router = Router()
storage = MemoryStorage()



class MenuStates(StatesGroup):
    ASSORTMENT = State()
    MAIN = State()
    DISCOUNTS = State()
    CATEGORY = State()
    VACANCY_INPUT = State()
    PROMOTIONS = State()
    PROMOTION_DETAILS = State()


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    main_menu = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Скидки"), KeyboardButton(text="Акции")],
            [KeyboardButton(text="Магазины"), KeyboardButton(text="Вакансии")],
            [KeyboardButton(text="Ассортимент")]
        ],
        resize_keyboard=True
    )
    await state.set_state(MenuStates.MAIN)  # Устанавливаем состояние "MAIN"
    await message.answer(
        "Добрый день! Пожалуйста, напишите /start для начала работы с ботом.\n"
        "Если вам нужна помощь, напишите /help для получения информации.",
        reply_markup=main_menu
    )
    await rq.set_user(message.from_user.id)


@router.message(Command('help'))
async def cmd_help(message: Message):
    await message.answer('Это команда /help')

@router.message(F.text == "Скидки")
async def discounts_menu(message: Message, state: FSMContext):

    discounts_menu = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Кошки"), KeyboardButton(text="Собаки")],
            [KeyboardButton(text="Другие"), KeyboardButton(text="Главное меню")]
        ],
        resize_keyboard=True,input_field_placeholder="Cкидки"
    )
    await state.set_state(MenuStates.DISCOUNTS)  # Устанавливаем состояние "DISCOUNTS"
    await message.answer("Выберите категорию скидок:", reply_markup=discounts_menu)





@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    main_menu = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Скидки"), KeyboardButton(text="Акции")],
            [KeyboardButton(text="Магазины"), KeyboardButton(text="Вакансии")],
            [KeyboardButton(text="Ассортимент")]
        ],
        resize_keyboard=True
    )
    await state.set_state(MenuStates.MAIN)  # Устанавливаем состояние "MAIN"
    await message.answer("Добрый день. Выберите пункт меню:", reply_markup=main_menu)

@router.message(F.text == "Главное меню")
async def go_to_main_menu(message: Message, state: FSMContext):
    try:
        main_menu = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="Скидки"), KeyboardButton(text="Акции")],
                [KeyboardButton(text="Магазины"), KeyboardButton(text="Вакансии")],
                [KeyboardButton(text="Ассортимент")]
            ],
            resize_keyboard=True
        )
        await state.set_state(MenuStates.MAIN)  # Возвращаем пользователя в состояние "MAIN"
        await message.answer("Вы вернулись в главное меню", reply_markup=main_menu)
    except Exception as e:
        logging.error(f"Ошибка при возвращении в главное меню: {e}")
        await message.answer("Произошла ошибка при возврате в главное меню. Попробуйте снова.")

@router.message(F.text == "Вакансии")
async def vacancy_input(message: Message, state: FSMContext):
    vacancy_menu = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Главное меню")]  # Кнопка "Главное меню"
        ],
        resize_keyboard=True
    )
    await state.set_state(MenuStates.VACANCY_INPUT)  # Устанавливаем состояние "VACANCY_INPUT"
    await message.answer("Введите текст объявления поиска работника:", reply_markup=vacancy_menu)

@router.message(MenuStates.VACANCY_INPUT)
async def handle_vacancy_text(message: Message, state: FSMContext):
    # Здесь можно обработать текст объявления, например, сохранить его или отправить в чат
    vacancy_text = message.text
    # Например, выводим обратно введённый текст
    await message.answer(f"Ваше объявление: {vacancy_text}\nСпасибо! Можете вернуться в главное меню.")
    await state.set_state(MenuStates.MAIN)  # Возвращаем состояние в главное меню

@router.message(F.text == "Акции")
async def promotions_menu(message: Message, state: FSMContext):
    promotions_menu = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="1+1=3"),KeyboardButton(text="1+1=-20%")],
            [KeyboardButton(text="День рождения -10%"),KeyboardButton(text="Главное меню")],
        ],
        resize_keyboard=True
    )
    await state.set_state(MenuStates.PROMOTIONS)  # Устанавливаем состояние "PROMOTIONS"
    await message.answer("Выберите акцию:", reply_markup=promotions_menu)

@router.message(F.text == "1+1=3")
async def promotion_1_plus_1_menu(message: Message, state: FSMContext):
    promotion_menu = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Товары участвующие в акции"),KeyboardButton(text="Назад")],
        ],
        resize_keyboard=True
    )
    await state.set_state(MenuStates.PROMOTION_DETAILS)  # Состояние для подменю акции
    await message.answer("Выберите действие:", reply_markup=promotion_menu)


@router.message(F.text == "1+1=-20%")
async def promotion_1_plus_20_menu(message: Message, state: FSMContext):
    promotion_menu = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Товары участвующие в акции"),KeyboardButton(text="Назад")],
        ],
        resize_keyboard=True
    )
    await state.set_state(MenuStates.PROMOTION_DETAILS)
    await message.answer("Выберите действие:", reply_markup=promotion_menu)


@router.message(F.text == "День рождения -10%")
async def birthday_promotion_menu(message: Message, state: FSMContext):
    promotion_menu = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Товары участвующие в акции"),KeyboardButton(text="Назад")]
        ],
        resize_keyboard=True
    )
    await state.set_state(MenuStates.PROMOTION_DETAILS)
    await message.answer("Выберите действие:", reply_markup=promotion_menu)


# Обработчик для кнопки "Товары участвующие в акции"
@router.message(F.text == "Товары участвующие в акции")
async def promotion_items(message: Message, state: FSMContext):
    # Здесь отправляем список товаров, участвующих в акции
    await message.answer("Список товаров, участвующих в акции:\n- Товар 1\n- Товар 2\n- Товар 3")


# Обработчик для кнопки "Назад" (возвращает на предыдущее меню с акциями)
@router.message(F.text == "Назад")
async def go_back_to_promotions(message: Message, state: FSMContext):
    promotions_menu = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="1+1=3"),KeyboardButton(text="1+1=-20%")],
            [KeyboardButton(text="День рождения -10%"),KeyboardButton(text="Главное меню")],
        ],
        resize_keyboard=True
    )
    await state.set_state(MenuStates.PROMOTIONS)  # Возвращаем состояние для меню акций
    await message.answer("Вы вернулись в меню акций:", reply_markup=promotions_menu)

@router.message(F.text == "Магазины")
async def stores_menu(message: Message, state: FSMContext):
    stores_menu = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Магазин №1"),KeyboardButton(text="Магазин №2")],
            [KeyboardButton(text="Магазин №3"),KeyboardButton(text="Главное меню")]
        ],
        resize_keyboard=True
    )
    await state.set_state(MenuStates.MAIN)  # Состояние "MAIN" для возврата в главное меню
    await message.answer("Выберите магазин:", reply_markup=stores_menu)

@router.message(F.text == "Магазин №1")
async def store_1(message: Message, state: FSMContext):
    store_menu = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Магазины")]
        ],
        resize_keyboard=True
    )
    await state.set_state(MenuStates.MAIN)  # Состояние для возврата в главное меню
    await message.answer(
        "Магазин №1:\nАдрес: Улица Пушкина, дом Колотушкина\nЧасы работы: с 9:00 до 21:00\n"
        "Посмотреть на карте: [Google Maps](https://maps.google.com/?q=Улица+Пушкина,дом+Колотушкина)",
        reply_markup=store_menu,
        parse_mode="Markdown"
    )


@router.message(F.text == "Магазин №2")
async def store_2(message: Message, state: FSMContext):
    store_menu = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Магазины")]
        ],
        resize_keyboard=True
    )
    await state.set_state(MenuStates.MAIN)  # Состояние для возврата в главное меню
    await message.answer(
        "Магазин №2:\nАдрес: Проспект Ленина, 42\nЧасы работы: с 10:00 до 22:00\n"
        "Посмотреть на карте: [Google Maps](https://maps.google.com/?q=Проспект+Ленина,42)",
        reply_markup=store_menu,
        parse_mode="Markdown"
    )


@router.message(F.text == "Магазин №3")
async def store_3(message: Message, state: FSMContext):
    store_menu = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Магазины")]
        ],
        resize_keyboard=True
    )
    await state.set_state(MenuStates.MAIN)  # Состояние для возврата в главное меню
    await message.answer(
        "Магазин №3:\nАдрес: Бульвар Шевченко, 17\nЧасы работы: с 8:00 до 20:00\n"
        "Посмотреть на карте: [Google Maps](https://maps.google.com/?q=Бульвар+Шевченко,17)",
        reply_markup=store_menu,
        parse_mode="Markdown"
    )

@router.message(F.text == "Ассортимент")
async def assortment_menu(message: Message, state: FSMContext):
    try:
        assortment_menu = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="Корма для собак"), KeyboardButton(text="Корма для кошек")],
                [KeyboardButton(text="Корма для птиц"), KeyboardButton(text="Игрушки для собак")],
                [KeyboardButton(text="Игрушки для кошек"), KeyboardButton(text="Лакомства для животных")],
                [KeyboardButton(text="Клетки"), KeyboardButton(text="Аквариумы")],
                [KeyboardButton(text="Животные"), KeyboardButton(text="Главное меню")]
            ],
            resize_keyboard=True
        )
        # Оставляем состояние MAIN для повторного использования
        await state.set_state(MenuStates.MAIN)
        await message.answer("Выберите категорию товаров:", reply_markup=assortment_menu)
    except Exception as e:
        logging.error(f"Ошибка при обработке кнопки Ассортимент: {e}")
        await message.answer("Произошла ошибка при обработке вашего запроса. Попробуйте снова.")

@router.message(F.text == "Скидки")
async def catalog(message:Message):
    await message.answer("Выберите категорию", reply_markup=await kb.categories())

@router.callback_query(F.data.startswith("category_"))
async def category(callback= CallbackQuery):
    await callback.answer("Вы выбрали категори")
    await callback.message.answer('Выберите товар по категории',
                                  reply_markup=await kb.items(callback.data.split('_')[1]))


@router.callback_query(F.data.startswith("item_"))
async def item_callback(callback: CallbackQuery):
    item_id = int(callback.data.split("_")[1])

    async with async_session() as session:
        item = await session.get(Item, item_id)

        if item is None:
            await callback.message.answer("Извините, товар не найден.")
            return

        await callback.message.answer(f"Товар: {item.name}\nЦена: {item.price}\nСкидка: {item.discount}%")



