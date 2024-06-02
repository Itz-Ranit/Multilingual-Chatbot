from translate import Translator
from googlesearch import search
import requests
from bs4 import BeautifulSoup


def translate_text(text, target_language, source_language='auto'):
    print(f"Translating '{text}' to '{target_language}' from '{source_language}'")
    translator = Translator(to_lang=target_language, from_lang=source_language)
    translation = translator.translate(text)
    print(f"Translation: {translation}")
    return translation


def fetch_answer(query):
    try:
        # Use Google search to fetch the answer
        search_results = list(search(query, num_results=1))
        if search_results:
            return search_results[0]
    except Exception as e:
        print(f"Error fetching answer: {e}")
    return None


def extract_answer_content(url, max_chars=500):
    try:
        # Send a GET request to the URL
        response = requests.get(url)
        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        # Extract relevant information (e.g., paragraph text)
        paragraphs = soup.find_all('p')
        content = ' '.join([paragraph.text for paragraph in paragraphs])
        # Limit the content to a certain number of characters
        truncated_content = content[:max_chars]
        return truncated_content
    except Exception as e:
        print(f"Error extracting answer content: {e}")
    return None


def chatbot():
    print("Welcome to the Multilingual Chatbot!")
    print("Type 'exit' to end the conversation.")

    while True:
        user_input = input("You: ")

        if user_input.lower() in ['exit', 'quit', 'bye']:
            print("Chatbot: Goodbye!")
            break

        # Detect language of user input
        source_language = 'en' if user_input.isascii() else 'bn'

        # Translate user input to English
        english_input = translate_text(user_input, 'en', source_language)

        # Fetch answer from the web
        answer_url = fetch_answer(english_input)

        if answer_url:
            print(f"Chatbot (English): I found an answer: {answer_url}")

            # Extract concise content from the webpage
            concise_answer = extract_answer_content(answer_url, max_chars=60)

            if concise_answer:
                # Translate the answer to Bengali
                bengali_answer = translate_text(concise_answer, 'bn', 'en')
                print(f"Chatbot (Bengali): {bengali_answer}")
            else:
                print("Chatbot (Bengali): Sorry, I couldn't find a concise answer.")
        else:
            print("Chatbot (Bengali): Sorry, I couldn't find an answer.")


if __name__ == "__main__":
    chatbot()
