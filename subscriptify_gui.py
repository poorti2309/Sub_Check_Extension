import requests
from bs4 import BeautifulSoup
import spacy
import streamlit as st
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

def get_website_text(url):
    try:
        # Launch Playwright and open the browser
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)  # Run in headless mode
            context = browser.new_context()
            page = context.new_page()

            # Go to the target URL
            page.goto(url, timeout=60000)  # Wait for the page to load completely

            # Wait for all dynamic content to load
            page.wait_for_load_state('networkidle')

            # Get the fully rendered HTML content
            content = page.content()

            # Parse the content with BeautifulSoup
            soup = BeautifulSoup(content, 'html.parser')
            text = soup.get_text(separator=' ', strip=True)

            # Close the browser
            browser.close()

            return text
    except Exception as e:
        return f"Error: Failed to fetch the website with Playwright. {str(e)}"


def analyze_subscription(text):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text.lower())
    
    subscription_keywords = {"subscribe", "membership", "premium", "paywall", "pricing", "unlimited access", "trial"}
    found_keywords = {token.text for token in doc if token.text in subscription_keywords}
    
    if found_keywords:
        if "free trial" in text.lower() or "limited access" in text.lower():
            return "Freemium Model: Some content is free, but full access requires a subscription."
        return "Paid Subscription Required: This website seems to require a membership."
    
    return "Free Access: This website appears to be free to use."

def main():
    st.title("Subscriptify - Website Subscription Checker")
    st.write("Enter a website URL to check its subscription model.")
    
    url = st.text_input("Website URL:")
    if st.button("Check Subscription"):
        if url.strip():
            text = get_website_text(url.strip())
            if text and not text.startswith("Error"):
                result = analyze_subscription(text)
                st.success(result)
            else:
                st.error("Unable to fetch website content. The website may block scraping.")
        else:
            st.warning("Please enter a valid URL.")

if __name__ == "__main__":
    main()
