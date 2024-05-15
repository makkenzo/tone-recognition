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
    positive_sentences = [sentence for sentence in blob.sentences if sentence.sentiment.polarity > 0]
    negative_sentences = [sentence for sentence in blob.sentences if sentence.sentiment.polarity < 0]
    neutral_count = total_sentences - len(positive_sentences) - len(negative_sentences)

    positive_count = len(positive_sentences)
    negative_count = len(negative_sentences)
    average_positive_polarity = (
        sum(sentence.sentiment.polarity for sentence in positive_sentences) / positive_count if positive_count else 0
    )
    average_negative_polarity = (
        sum(sentence.sentiment.polarity for sentence in negative_sentences) / negative_count if negative_count else 0
    )
    most_positive = (
        max(positive_sentences, key=lambda sentence: sentence.sentiment.polarity, default="").string
        if positive_sentences
        else "Нет данных"
    )
    most_negative = (
        min(negative_sentences, key=lambda sentence: sentence.sentiment.polarity, default="").string
        if negative_sentences
        else "Нет данных"
    )

    if positive_count > negative_count and positive_count > neutral_count:
        sentiment_overall = "Положительный"
    elif negative_count > positive_count and negative_count > neutral_count:
        sentiment_overall = "Отрицательный"
    else:
        sentiment_overall = "Нейтральный"

    return (
        sentiment_overall,
        positive_count,
        negative_count,
        neutral_count,
        total_sentences,
        average_positive_polarity,
        average_negative_polarity,
        most_positive,
        most_negative,
    )


@dp.message_handler(commands=["start"])
async def send_welcome(message: types.Message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("Примеры"))
    await message.answer("Привет! Нажми на кнопку 'Примеры', чтобы увидеть дополнительные опции.", reply_markup=markup)


@dp.message_handler(lambda message: message.text == "Примеры")
async def show_examples(message: types.Message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(
        types.KeyboardButton("Нейтральное"), types.KeyboardButton("Позитивное"), types.KeyboardButton("Негативное")
    )
    await message.answer("Выберите пример:", reply_markup=markup)


@dp.message_handler(lambda message: message.text in ["Нейтральное", "Позитивное", "Негативное"])
async def send_test_message(message: types.Message):
    test_messages = {
        "Нейтральное": "Just a reminder that our weekly team meeting is scheduled for 10 AM today in conference room B. Make sure to bring any updates or progress reports.",
        "Позитивное": "Wow, what an amazing turnout at yesterday's charity event! Thanks to everyone who volunteered their time and resources to make it a huge success. Together, we're making a real difference in our community. Let's keep up the great work!",
        "Негативное": "I can't believe the incompetence displayed in yesterday's presentation. It was an embarrassment, and awful, unacceptable. We've invested time and resources into this project, and to see it butchered like that is beyond disappointing. We need to get our act together and start producing quality work. This level of mediocrity is dragging us all down, and if we don't shape up, there will be serious consequences.",
    }
    chosen_message = test_messages[message.text]
    sentiment_analysis = analyze_sentiment(chosen_message)
    response_message = (
        f"Тестовое сообщение:\n\n'{chosen_message}'\n\n"
        f"📊 Общая тональность: {sentiment_analysis[0]}\n"
        f"😊 Положительные предложения: {sentiment_analysis[1]} из {sentiment_analysis[4]} (Средняя полярность: {sentiment_analysis[5]:.2f})\n"
        f"👍 Самое позитивное предложение: '{sentiment_analysis[7]}'\n"
        f"😡 Отрицательные предложения: {sentiment_analysis[2]} из {sentiment_analysis[4]} (Средняя полярность: {sentiment_analysis[6]:.2f})\n"
        f"👎 Самое негативное предложение: '{sentiment_analysis[8]}'\n"
        f"😐 Нейтральные предложения: {sentiment_analysis[3]} из {sentiment_analysis[4]}"
    )
    await message.answer(response_message)


@dp.message_handler(content_types=["text"])  # Этот обработчик будет перехватывать все текстовые сообщения
async def handle_all_text_messages(message: types.Message):
    if message.text not in ["Примеры", "Нейтральное", "Позитивное", "Негативное"]:
        sentiment_analysis = analyze_sentiment(message.text)
        await message.reply(
            f"📊 Общая тональность: {sentiment_analysis[0]}\n"
            f"😊 Положительные предложения: {sentiment_analysis[1]} из {sentiment_analysis[4]} (Средняя полярность: {sentiment_analysis[5]:.2f})\n"
            f"👍 Самое позитивное предложение: '{sentiment_analysis[7]}'\n"
            f"😡 Отрицательные предложения: {sentiment_analysis[2]} из {sentiment_analysis[4]} (Средняя полярность: {sentiment_analysis[6]:.2f})\n"
            f"👎 Самое негативное предложение: '{sentiment_analysis[8]}'\n"
            f"😐 Нейтральные предложения: {sentiment_analysis[3]} из {sentiment_analysis[4]}"
        )


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
