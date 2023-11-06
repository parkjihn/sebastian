import speech_recognition as sr
import pyttsx3
import datetime
import requests
import random
import sqlite3

# Initialize SQLite database
conn = sqlite3.connect('sebastian.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS interactions
                  (timestamp TEXT, query TEXT, response TEXT)''')
conn.commit()

def save_interaction(query, response):
    cursor.execute("INSERT INTO interactions VALUES (?, ?, ?)",
                   (datetime.datetime.now(), query, response))
    conn.commit()

def get_last_query():
    cursor.execute("SELECT query FROM interactions ORDER BY timestamp DESC LIMIT 1")
    row = cursor.fetchone()
    if row:
        return row[0]
    return None

# Function to listen to the user's voice
def listen():
    r = sr.Recognizer()
    mic = sr.Microphone()
    with mic as source:
        print("Listening...")
        audio = r.listen(source)
    return r.recognize_google(audio)

# Function to fetch news
def fetch_news():
    api_key = "4f457042b3c14b41a9a079bf914c0373"  # Replace with your actual API key
    url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={api_key}"
    response = requests.get(url)
    news_data = response.json()
    headlines = []

    for article in news_data['articles'][:5]:
        headlines.append(article['title'])

    news = "Here are the top 5 news headlines: " + ", ".join(headlines)
    return news

# Function to get cryptocurrency price
def get_crypto_price(crypto_name):
    url = f'https://api.coingecko.com/api/v3/simple/price?ids={crypto_name}&vs_currencies=usd'
    response = requests.get(url)
    data = response.json()
    if crypto_name in data:
        return f"The current price of {crypto_name.capitalize()} is ${data[crypto_name]['usd']} USD."
    else:
        return "I couldn't find that cryptocurrency."


# Function to respond based on the recognized text
def respond(text):
    last_query = get_last_query()

    greetings = ["hello", "hi", "hey", "greetings"]
    farewells = ["bye", "goodbye", "see you later"]

    if any(word in text for word in greetings):
        response = random.choice(["Hello, how may I assist you?", "Hi, what can I do for you?", "Greetings, how can I help?"])
    elif "how are you" in text:
        response = random.choice(["I'm just a program, so I don't have feelings, but thank you for asking.", "I'm doing well, thank you. How can I assist you?", "Quite well, thank you. What do you need?"])
    elif "news" in text:
        response = fetch_news()
    elif "date" in text:
        response = f"Today's date is {datetime.datetime.now().strftime('%Y-%m-%d')}"
    elif "time" in text:
        response = f"The current time is {datetime.datetime.now().strftime('%H:%M:%S')}"

    elif "crypto price" in text:
        words = text.split()
        if 'of' in words:
            index_of_of = words.index('of') + 1
            crypto_name = words[index_of_of]
        else:
            crypto_name = words[-1]
        response = get_crypto_price(crypto_name.lower())

    elif any(word in text for word in farewells):
        response = random.choice(["Goodbye!", "See you later!", "Till next time!"])


    else:
        response = random.choice(["I'm sorry, I didn't understand that.", "Could you please repeat?", "I apologize, I couldn't get that."])



    save_interaction(text, response)
    return response

def main():
    engine = pyttsx3.init()
    engine.setProperty('voice', 'HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\TTS_MS_EN-US_DAVID_11.0')

    while True:
        try:
            voice_note = listen().lower()
            print("You said: {}".format(voice_note))

            response = respond(voice_note)
            print("Sebastian says: {}".format(response))

            engine.say(response)
            engine.runAndWait()

            if "bye" in voice_note:
                break

        except sr.UnknownValueError:
            print("Sorry, I could not understand the audio.")
        except sr.RequestError as e:
            print(f"Could not request results; {e}")

if __name__ == "__main__":
    main()
