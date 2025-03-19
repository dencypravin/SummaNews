import requests
import html
from bs4 import BeautifulSoup
from transformers import pipeline
from textblob import TextBlob
from gtts import gTTS
import os

# Load summarization model once
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def summarize_text(text, max_length=100):
    """Summarize long text using Hugging Face transformers."""
    if len(text.split()) < 20:  
        return text  # Return original text if too short
    summary = summarizer(text, max_length=max_length, min_length=30, do_sample=False)
    return summary[0]["summary_text"]

def clean_html(raw_html):
    """Remove HTML tags and extract plain text."""
    soup = BeautifulSoup(raw_html, "html.parser")
    text = soup.get_text(separator=" ")  # Extract text with spaces
    text = html.unescape(text)  # Decode HTML entities
    text = text.replace("\xa0", " ")  # Replace non-breaking spaces
    text = text.replace("\n", " ").strip()  # Remove excessive newlines
    return text

def get_news(company_name):
    """Fetch and summarize the latest news articles about a company."""
    rss_url = f"https://news.google.com/rss/search?q={company_name}"
    response = requests.get(rss_url)

    if response.status_code != 200:
        print("Error fetching news")
        return []

    soup = BeautifulSoup(response.content, "xml")
    articles = []

    for item in soup.find_all("item")[:10]:
        title = item.title.text
        link = item.link.text
        raw_description = item.description.text if item.description else "Summary not available"

        # Clean HTML from the description
        description = clean_html(raw_description)

        # Attempt to fetch full article content
        try:
            article_response = requests.get(link)
            article_soup = BeautifulSoup(article_response.content, "html.parser")
            paragraphs = article_soup.find_all("p")
            full_text = " ".join([p.text for p in paragraphs[:5]])  # First 5 paragraphs
            content = full_text if len(full_text) > len(description) else description
        except Exception as e:
            content = description  # Fallback to description if request fails
            print(f"Error fetching full article: {e}")

        summary = summarize_text(content)

        articles.append({"title": title, "link": link, "summary": summary})

    return articles

def analyze_sentiment(text):
    analysis = TextBlob(text)
    if analysis.sentiment.polarity > 0:
        return "Positive"
    elif analysis.sentiment.polarity < 0:
        return "Negative"
    else:
        return "Neutral"
    
def comparative_analysis(articles):
    """Analyze sentiment distribution and topic overlap."""
    sentiment_counts = {"Positive": 0, "Negative": 0, "Neutral": 0}

    for article in articles:
        sentiment = analyze_sentiment(article["summary"])
        sentiment_counts[sentiment] += 1

    return sentiment_counts

def text_to_speech(text, filename="output.mp3"):
    """Convert text to Hindi speech and save as an audio file."""
    tts = gTTS(text, lang="hi")  # 'hi' for Hindi
    tts.save(filename)
    print(f"🔊 Hindi Speech saved as {filename}")
    return filename

