from aiogram import  Bot, F, Dispatcher
from aiogram.filters import  Command, CommandStart,StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message


TOKEN = '' # Пиши свой токен бота друган )))))
storage = MemoryStorage()
bot = Bot(token=TOKEN)
dp = Dispatcher()

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

@dp.message(Command(commands='start'))
async def process_start(message: Message):
    await message.answer('Я бот вычесляющий норму калорий')

@dp.message(F.text == 'colories')
async def set_message(message: Message, state: FSMContext):
    await message.answer('Введите ваш возраст: ')
    await  state.set_state(UserState.age)

@dp.message(StateFilter(UserState.age))
async def set_growth(message: Message, state: FSMContext):
    await state.update_data(age=message.text)
    await message.answer('Введите ваш рост: ')
    await state.set_state(UserState.growth)

@dp.message(StateFilter(UserState.growth))
async def set_weight(message: Message, state: FSMContext):
    await state.update_data(growth=message.text)
    await message.answer('Введите свой вес: ')
    await state.set_state(UserState.weight)

@dp.message(StateFilter(UserState.weight))
async def send_calories(message: Message, state: FSMContext):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    print(data['weight'])
    res =  10 * int(data['weight']) + 6.25 * int(data['growth']) - 5 * int(data['age']) + 5
    await message.answer(f'Ваша норма калорий {str(res)}')
    await state.clear()

if __name__ == '__main__':
    dp.run_polling(bot)

