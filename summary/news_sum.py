from utils import get_news, analyze_sentiment, comparative_analysis, text_to_speech

# Ask the user for a company name
company_name = input("Enter a company name: ").strip()  # Ensure no extra spaces

# Debugging: Print the company name to check if it's correctly entered
print(f"\n Fetching news for: {company_name}")

# Fetch news articles for the entered company
news_articles = get_news(company_name)

# Debugging: Check if news_articles actually contains data
if not news_articles:
    print(" No news articles found. Try another company.")
    exit()  # Stop execution if no articles found

# Run Comparative Analysis
sentiment_report = comparative_analysis(news_articles)

# Generate a Hindi summary
hindi_text = f"{company_name} की खबरों का संक्षेपण: सकारात्मक खबरें {sentiment_report['Positive']}, नकारात्मक खबरें {sentiment_report['Negative']}, और तटस्थ खबरें {sentiment_report['Neutral']} हैं।"

# Convert text to speech
audio_file = text_to_speech(hindi_text, f"{company_name}_summary.mp3")

# Save results to a dynamically named file
filename = f"{company_name}_summarized_news.txt"
with open(filename, "w", encoding="utf-8") as file:
    file.write(f"Company: {company_name}\n")
    file.write(f"Sentiment Distribution: {sentiment_report}\n")
    file.write("=" * 80 + "\n")

    for article in news_articles:
        title = article['title']
        summary = article['summary']
        sentiment = analyze_sentiment(summary)
        
        file.write(f"Title: {title}\n")
        file.write(f"Summary: {summary}\n")
        file.write(f"Sentiment: {sentiment}\n")
        file.write("-" * 50 + "\n")

print(f"\n✅ Hindi speech file generated: {company_name}_summary.mp3")
print(f"✅ Summarized news saved in {filename}")
