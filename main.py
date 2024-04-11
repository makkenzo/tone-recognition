from textblob import TextBlob


def analyze_sentiment(text):
    blob = TextBlob(text)
    sentences_sentiment = []

    for sentence in blob.sentences:
        sentiment = 0
        words = sentence.words

        for i, word in enumerate(words):
            if word == "not" and i + 1 < len(words):
                next_word_sentiment = TextBlob(words[i + 1]).sentiment.polarity
                sentiment -= next_word_sentiment
            else:
                sentiment += TextBlob(word).sentiment.polarity
        sentences_sentiment.append(sentiment)

    total_sentiment = sum(sentences_sentiment) / len(sentences_sentiment)

    if total_sentiment > 0:
        return "Позитивная"
    elif total_sentiment < 0:
        return "Негативная"
    else:
        return "Нейтральная"


positive_message = """
It was a beautiful day, the sun was shining, the sky was clear and cloudless. A gentle breeze played with the leaves on the trees, creating a peaceful atmosphere. People on the streets were smiling and enjoying the beautiful weather.

However, despite all this, I had a strange feeling of anxiety in my soul. Perhaps it was because of an upcoming meeting with a former colleague with whom I had unresolved conflicts. I was worried about how our communication would go and worried that I might say something inappropriate.

I soon made my way to the meeting point, watching the streets slowly fill with people. My thoughts were mixed: on the one hand, I was glad to have the opportunity to resolve our differences, on the other hand, I felt anxious about the upcoming conversation.

When I met with a former colleague, our communication went much better than I expected. We discussed our problems and found compromise solutions. It was a very positive experience that left me delighted.

However, as the evening approached, my anxiety began to increase. I remembered our meeting and began to analyze our every word. Doubts and fears took hold of me again, and I began to doubt myself and my actions.

Thus, despite the beautiful weather and the successful resolution of the conflict with a colleague, my emotional component remained mixed. Although the meeting was a positive event, I still felt inner restlessness and anxiety.
"""

negative_message = """
Today was a terrible day. Nothing went right from the moment I woke up. 
I spilled coffee on my favorite shirt, missed the bus to work, and then got reprimanded by my boss for being late. 
To make matters worse, it started raining heavily on my way home, and I got completely soaked. 
I'm feeling so frustrated and miserable right now.
"""

sentiment_label = analyze_sentiment(positive_message)

print("Тональность сообщения:", sentiment_label)
