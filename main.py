import logging
from aiogram import Bot, Dispatcher, executor, types
from textblob import TextBlob
from langdetect import detect, DetectorFactory, lang_detect_exception
from polyglot.text import Text as PText


API_TOKEN = "7041320804:AAGRjZj8BxaXyBc6p_h7eGOrNx_SSPWl_BY"

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

DetectorFactory.seed = 0


def analyze_sentiment(text):
    try:
        lang = detect(text)
    except lang_detect_exception.LangDetectException:
        return "Нейтральная"

    try:
        if lang == "ru":
            poly_text = PText(text, hint_language_code="ru")
            scores = [s.polarity for s in poly_text.sentences if hasattr(s, "polarity")]
            if len(scores) > 0:
                sentiment = sum(scores) / len(scores)
            else:
                return "Нейтральная"
        else:
            blob = TextBlob(text)
            scores = [sentence.sentiment.polarity for sentence in blob.sentences]
            if len(scores) > 0:
                sentiment = sum(scores) / len(scores)
            else:
                return "Нейтральная"
    except Exception as e:
        print(f"Unexpected error during sentiment analysis: {str(e)}")
        return "Нейтральная"

    if sentiment > 0:
        return "Позитивная"
    elif sentiment < 0:
        return "Негативная"
    else:
        return "Нейтральная"


@dp.message_handler()
async def send_welcome(message: types.Message):
    sentiment_label = analyze_sentiment(message.text)
    await message.answer(f"Тональность сообщения: {sentiment_label}")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
