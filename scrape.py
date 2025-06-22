# from selenium.webdriver import Remote, ChromeOptions
# from selenium.webdriver.chromium.remote_connection import ChromiumRemoteConnection
# from bs4 import BeautifulSoup
# SBR_WEBDRIVER='https://brd-customer-hl_b0723d84-zone-ai_scraper:bna6y4cz57o7@brd.superproxy.io:9515'

# def scrape_website(website):
#     print("launching chrome browser..")

    

# def scrape_website(website):
#     print("Connecting to Scraping Browser...")
#     sbr_connection = ChromiumRemoteConnection(SBR_WEBDRIVER, "goog", "chrome")
#     with Remote(sbr_connection, options=ChromeOptions()) as driver:
#         driver.get(website)
#         print("Waiting captcha to solve...")
#         solve_res = driver.execute(
#             "executeCdpCommand",
#             {
#                 "cmd": "Captcha.waitForSolve",
#                 "params": {"detectTimeout": 10000},
#             },
#         )
#         print("Captcha solve status:", solve_res["value"]["status"])
#         print("Navigated! Scraping page content...")
#         html = driver.page_source
#         return html
    
# def extract_body_content(html_content):
#     soup = BeautifulSoup(html_content, "html.parser")
#     body_content = soup.body
#     if body_content:
#         return str(body_content)
#     return ""


# def clean_body_content(body_content):
#     soup = BeautifulSoup(body_content, "html.parser")

#     for script_or_style in soup(["script", "style"]):
#         script_or_style.extract()

#     # Get text or further process the content
#     cleaned_content = soup.get_text(separator="\n")
#     cleaned_content = "\n".join(
#         line.strip() for line in cleaned_content.splitlines() if line.strip()
#     )

#     return cleaned_content


# def split_dom_content(dom_content, max_length=6000):
#     return [
#         dom_content[i : i + max_length] for i in range(0, len(dom_content), max_length)
#     ]

import time
import selenium.webdriver as webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup

# Pinecone & LangChain
import pinecone
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Pinecone
from langchain.schema import Document
import os

# ----------- Web Scraping -----------
def scrape_website(website):
    print("Launching Chrome browser...")

    chrome_driver_path = "./chromedriver.exe"  # Use chromedriver path suitable for your system
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=Service(chrome_driver_path), options=options)

    try:
        driver.get(website)
        print("Page loaded...")
        time.sleep(10)
        html = driver.page_source
        return html
    finally:
        driver.quit()

# ----------- Extract & Clean -----------
def extract_body_content(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    body_content = soup.body
    if body_content:
        return str(body_content)
    return ""

def clean_body_content(body_content):
    soup = BeautifulSoup(body_content, "html.parser")
    for script_or_style in soup(["script", "style"]):
        script_or_style.extract()

    cleaned_content = soup.get_text(separator="\n")
    cleaned_content = "\n".join(
        line.strip() for line in cleaned_content.splitlines() if line.strip()
    )
    return cleaned_content

def split_dom_content(dom_content, max_length=6000):
    return [dom_content[i: i + max_length] for i in range(0, len(dom_content), max_length)]

# ----------- Pinecone Integration -----------
def init_pinecone():
    pinecone.init(
        api_key=os.getenv("PINECONE_API_KEY"),     # Set in your environment
        environment=os.getenv("PINECONE_ENV")      # e.g., "gcp-starter"
    )

def index_to_pinecone(chunks, index_name="web-scrape-index"):
    embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))
    documents = [Document(page_content=chunk) for chunk in chunks]
    vectorstore = Pinecone.from_documents(documents, embedding=embeddings, index_name=index_name)
    print("✅ Successfully stored in Pinecone.")

# ----------- Main Flow -----------
if __name__ == "__main__":
    website_url = "https://example.com"  # Replace with your target URL
    html = scrape_website(website_url)

    body = extract_body_content(html)
    cleaned = clean_body_content(body)
    chunks = split_dom_content(cleaned)

    init_pinecone()
    index_to_pinecone(chunks)
