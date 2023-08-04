import chromadb
import requests
import re
import unidecode
import unicodedata
import torch
from transformers import LongformerTokenizer, LongformerModel
from fastapi import FastAPI
from readability import Readability
from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.parse import urlparse

# Reminder: code will needed commented out as you go so containers are not created twice etc.

tokenizer = LongformerTokenizer.from_pretrained('allenai/longformer-base-4096')
model = LongformerModel.from_pretrained('allenai/longformer-base-4096')

# pulls the text from the input url -> what will be our documents
# Written by Madhu Patel, with some slight changes
def check_by_url(txt_url):
    parsed_url = urlparse(txt_url)
    url = (f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path.rsplit('/', 1)[0]}/")
    # print(url)

    new_data = []
    page = urlopen(url=url).read()
    page = page.decode("utf-8")
    soup = BeautifulSoup(page, "html.parser")
    title = soup.find("title").get_text()

    # remove punctuations from title
    def remove_punctuation(title):
        punctuationfree = "".join([i for i in title if i not in string.punctuation])
        return punctuationfree

    css_class_to_remove = ("dp-highlighter")  # Replace with the CSS class you want to remove
    # Find <div> tags with the specified CSS class and remove their content
    div_tags = soup.find_all(["code", "pre"])
    for div_tag in div_tags:
        div_tag.clear()

    div_tags = soup.find_all("div", class_=css_class_to_remove)
    for div_tag in div_tags:
        div_tag.clear()

    # Fetch content of remaining tags
    content_with_style = ""
    p_tags_with_style = soup.find_all("p", style=True)
    for p_tag in p_tags_with_style:
        p_content = re.sub(r"\n", "", p_tag.get_text())
        content_with_style += p_content

    # Fetch content of <p> tags without style
    content_without_style = ""
    p_tags_without_style = soup.find_all("p", style=False)
    for p_tag in p_tags_without_style:
        p_content = re.sub(r"\n", "", p_tag.get_text())
        content_without_style += p_content

    # Replace Unicode characters in the content and remove duplicates
    normalized_content_with_style = re.sub(r"\s+", " ", content_with_style)  # Remove extra spaces
    normalized_content_with_style = normalized_content_with_style.replace("\r", "")  # Replace '\r' characters
    normalized_content_with_style = unicodedata.normalize("NFKD", normalized_content_with_style)
    normalized_content_with_style = unidecode.unidecode(normalized_content_with_style)

    normalized_content_without_style = re.sub(r"\s+", " ", content_without_style)  # Remove extra spaces
    normalized_content_without_style = normalized_content_without_style.replace("\r", "")  # Replace '\r' characters
    normalized_content_without_style = unicodedata.normalize("NFKD", normalized_content_without_style)
    normalized_content_without_style = unidecode.unidecode(normalized_content_without_style)

    normalized_content_with_style += normalized_content_without_style
    new_data = {"content": normalized_content_with_style}
    return new_data

# adds a single article to the collection
# data is a single item from the stack exchagne api response (one article)
# collection name is the name as the variable in the program, not in Docker, need to work this out
# ? better to pass an array of mutliple ?
# when adding an article:
# documents = the content of the article
# ids = article_id (given to the artile by stackexchange)
# metadatas = article title, article url
def addToCollection(collectionName, data: dict) -> None:
    # grab the content from the url that is in the data
    content = check_by_url(data['link'])
    content = content['content']
    
    # 
    collectionName.add(
        documents = [content],
        ids = [str(data['article_id'])],
        metadatas = [{'title': data['title'], 'url': data['link']}]
    )

# searches for articles most related the the input
def queryCollection(collectionName, queryIn: str, numResults: int) -> None:
    results = collectionName.query(
        query_texts = queryIn,
        n_results = numResults
    )
    print(results['metadatas'])

# before starting with chroma grab a list of articles to use
url = 'https://api.stackexchange.com/2.3/articles?order=desc&sort=activity&site=stackoverflow'
response = requests.get(url)
response = response.json()

# create our client -> port comes from docke
client = chromadb.HttpClient(host= 'localhost', port= 8000)
  
# # assume there is no data, fresh container
collection = client.create_collection(name= 'mainCollection')
collection = client.get_collection(name= 'mainCollection')

# for each article in the response we will add it to our collection
for i in response['items']:
     addToCollection(collection, i)

# you can now query against these articles
vector = "Introduction Ballerina"

# make a query
queryCollection (collection, vector, 3)

