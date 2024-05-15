import logging
from aiogram import Bot, Dispatcher, executor, types
from textblob import TextBlob

API_TOKEN = "7041320804:AAGRjZj8BxaXyBc6p_h7eGOrNx_SSPWl_BY"

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


def analyze_sentiment(text):
    blob = TextBlob(text)
    total_sentences = len(blob.sentences)
    positive_count = sum(1 for sentence in blob.sentences if sentence.sentiment.polarity > 0)
    negative_count = sum(1 for sentence in blob.sentences if sentence.sentiment.polarity < 0)
    neutral_count = total_sentences - positive_count - negative_count

    if positive_count > negative_count and positive_count > neutral_count:
        sentiment_overall = "Положительный"
    elif negative_count > positive_count and negative_count > neutral_count:
        sentiment_overall = "Отрицательный"
    else:
        sentiment_overall = "Нейтральный"

    return sentiment_overall, positive_count, negative_count, neutral_count, total_sentences


@dp.message_handler(commands=["start"])
async def send_welcome(message: types.Message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(types.KeyboardButton("Примеры"))
    await message.answer("Привет! Нажми на кнопку 'Примеры', чтобы увидеть дополнительные опции.", reply_markup=markup)


@dp.message_handler(lambda message: message.text == "Примеры")
async def show_examples(message: types.Message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(
        types.KeyboardButton("Нейтральное"), types.KeyboardButton("Позитивное"), types.KeyboardButton("Негативное")
    )
    await message.answer("Выберите номер:", reply_markup=markup)


@dp.message_handler(lambda message: message.text in ["Нейтральное", "Позитивное", "Негативное"])
async def send_test_message(message: types.Message):
    test_messages = {
        "Нейтральное": "Just a reminder that our weekly team meeting is scheduled for 10 AM today in conference room B. Make sure to bring any updates or progress reports.",
        "Позитивное": "Wow, what an amazing turnout at yesterday's charity event! Thanks to everyone who volunteered their time and resources to make it a huge success. Together, we're making a real difference in our community. Let's keep up the great work!",
        "Негативное": "I can't believe the incompetence displayed in yesterday's presentation. It was an embarrassment, and awful, unacceptable. We've invested time and resources into this project, and to see it butchered like that is beyond disappointing. We need to get our act together and start producing quality work. This level of mediocrity is dragging us all down, and if we don't shape up, there will be serious consequences.",
    }
    chosen_message = test_messages[message.text]
    sentiment_overall, positive_count, negative_count, neutral_count, total_sentences = analyze_sentiment(
        chosen_message
    )
    response_message = (
        f"Тестовое сообщение:\n\n{chosen_message}\n\n"
        f"Тональность: {sentiment_overall}\n"
        f"Положительные предложения: {positive_count}/{total_sentences}\n"
        f"Отрицательные предложения: {negative_count}/{total_sentences}\n"
        f"Нейтральные предложения: {neutral_count}/{total_sentences}"
    )
    await message.answer(response_message, reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler()  # Этот обработчик будет перехватывать все остальные текстовые сообщения
async def handle_all_other_messages(message: types.Message):
    sentiment_overall, positive_count, negative_count, neutral_count, total_sentences = analyze_sentiment(message.text)
    await message.answer(
        f"Тональность вашего сообщения: {sentiment_overall}\n"
        f"Положительные предложения: {positive_count}/{total_sentences}\n"
        f"Отрицательные предложения: {negative_count}/{total_sentences}\n"
        f"Нейтральные предложения: {neutral_count}/{total_sentences}"
    )


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
