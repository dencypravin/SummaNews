import streamlit as st
from summary.utils import get_news, analyze_sentiment, comparative_analysis, text_to_speech


st.title(" News Summarization & Sentiment Analysis")

# User input for company name
company_name = st.text_input("Enter a company name:", "")

if st.button("Analyze News"):
    if not company_name:
        st.warning(" Please enter a company name.")
    else:
        # Fetch news
        st.write(f" Fetching news for: {company_name}...")
        news_articles = get_news(company_name)

        if not news_articles:
            st.error("No news articles found. Try another company.")
        else:
            # Perform Sentiment Analysis
            sentiment_report = comparative_analysis(news_articles)

            # Display Sentiment Distribution
            st.subheader("Sentiment Distribution")
            st.write(sentiment_report)

            # Display Summarized News
            st.subheader(" Summarized News")
            for article in news_articles:
                st.write(f"**{article['title']}**")
                st.write(f" [Read more]({article['link']})")
                st.write(f" Summary: {article['summary']}")
                st.write(f" Sentiment: {analyze_sentiment(article['summary'])}")
                st.write("---")

            # Convert summary to Hindi speech
            hindi_text = f"{company_name} की खबरों का संक्षेपण: सकारात्मक खबरें {sentiment_report['Positive']}, नकारात्मक खबरें {sentiment_report['Negative']}, और तटस्थ खबरें {sentiment_report['Neutral']} हैं।"
            audio_file = text_to_speech(hindi_text, f"{company_name}_summary.mp3")

            # Provide download link for the audio
            st.subheader(" Hindi Audio Summary")
            st.audio(audio_file)

            st.success(f" Analysis complete for {company_name}!")
