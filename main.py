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
        return "Neutral", 0, 0, 0

    try:
        if lang == "ru":
            poly_text = PText(text, hint_language_code="ru")
            scores = [s.polarity for s in poly_text.sentences if hasattr(s, "polarity")]
            if len(scores) > 0:
                sentiment = sum(scores) / len(scores)
            else:
                return "Neutral", 0, 0, 0
        else:
            blob = TextBlob(text)
            scores = [sentence.sentiment.polarity for sentence in blob.sentences]
            if len(scores) > 0:
                sentiment = sum(scores) / len(scores)
            else:
                return "Neutral", 0, 0, 0
    except Exception as e:
        print(f"Unexpected error during sentiment analysis: {str(e)}")
        return "Neutral", 0, 0, 0

    positive_sentences = sum(1 for score in scores if score > 0)
    negative_sentences = sum(1 for score in scores if score < 0)
    neutral_sentences = sum(1 for score in scores if score == 0)
    total_sentences = len(scores)

    if sentiment > 0:
        sentiment_label = "Positive"
    elif sentiment < 0:
        sentiment_label = "Negative"
    else:
        sentiment_label = "Neutral"

    return sentiment_label, positive_sentences, negative_sentences, neutral_sentences, total_sentences


@dp.message_handler()
async def send_welcome(message: types.Message):
    sentiment_label, positive_sentences, negative_sentences, neutral_sentences, total_sentences = analyze_sentiment(
        message.text
    )
    await message.answer(
        f"🤖 We have processed your message and determined that your emotional coloring is - <b>{sentiment_label.capitalize()}</b>.\n\n"
        f"👍 Positive Sentences: {positive_sentences}/{total_sentences}\n"
        f"👎 Negative Sentences: {negative_sentences}/{total_sentences}\n"
        f"😐 Neutral Sentences: {neutral_sentences}/{total_sentences}",
        parse_mode=types.ParseMode.HTML,
    )


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
