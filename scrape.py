import argparse
import httpx
from parsel import Selector
from wordcloud import WordCloud
import re
import multidict
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import logging
import sys

parser = argparse.ArgumentParser(description="Google search script")
parser.add_argument("query", type=str, help="Search query")
args = parser.parse_args()
query = args.query
url = f"https://www.google.com/search?q={query}&num=100&hl=en&lr=lang_en"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.35"
}
try:
    
    response = httpx.get(url, headers=headers, follow_redirects=True)
    response.raise_for_status()
except httpx.HTTPError as exc:
    print(response)
    print(f"HTTP Exception for {exc.request.url} - {exc}")
    

selector = Selector(response.text)
results = []

container_xpath = '//div[starts-with(@class, "g")]'  # XPath for each search result container
link_xpath = './/a/@href'  # XPath for extracting the link from the result container
title_xpath = './/h3/text()'  # XPath for extracting the title from the result container
description_xpath = './/div[starts-with(@class, "VwiC3b")]//text()'  # XPath for extracting the description from the result container

# Extract data from the search results
containers = selector.xpath(container_xpath)
for container in containers:
    link = container.xpath(link_xpath).get()
    title = container.xpath(title_xpath).get()
    description = container.xpath(description_xpath).getall()

    if link and title:
        result = {
            "link": link,
            "title": title.strip(),
            "description": " ".join(description).strip() if description else ""
        }
        results.append(result)


def getFrequencyDictForText(sentence):
    fullTermsDict = multidict.MultiDict()
    tmpDict = {}

# making dict for counting frequencies
    for text in sentence.split(" "):
        if re.match("a|the|an|the|to|in|for|of|or|by|with|is|on|that|be", text):
            continue
        if not text.isalnum():
            continue
        if text.isdigit() and len(text) == 1:
            continue
        val = tmpDict.get(text, 0)
        tmpDict[text] = val + 1
    for key in tmpDict:
        fullTermsDict.add(key, tmpDict[key])
    return fullTermsDict

# Generate word cloud
text_data = ""
for result in results:
    text_data += result["title"] + " " + result["description"] + " "

# Count frequency of words
word_count = getFrequencyDictForText(text_data)

# Sort word count from high to low
sorted_word_count = sorted(word_count.items(), key=lambda x: x[1], reverse=True)
##print(sorted_word_count)

# Remove stopwords from sorted_word_count using NLTK library
nltk.download('stopwords', quiet=True)
stop_words = set(stopwords.words('english'))
sorted_word_count = [(word, freq) for word, freq in sorted_word_count if word not in stop_words]
sorted_word_count = [(word, freq) for word, freq in sorted_word_count if freq >= 2]

sorted_word_count_final = []
for word in sorted_word_count:
    sorted_word_count_final.append(word[0])

sorted_word_count_string = str(sorted_word_count_final)
sorted_word_count_string = sorted_word_count_string.replace("[", "").replace("]", "").replace(",", "").replace("'", "")

## print(sorted_word_count_string)

def extract_nouns(text):
    """
    Extracts all the nouns from a given text.
    """
    tokens = word_tokenize(text)
    tagged = nltk.pos_tag(tokens)
    nouns = [word for word, pos in tagged if pos.startswith('N') or (pos == 'CD') or (word.isdigit())]
    return nouns
# Extract only the nouns
nouns = str(extract_nouns(sorted_word_count_string))
words_to_remove = ["hours", "days", "weeks", "[", "]", ",", "'", "news", "site", "sites", "file", "web", "download" , "wikipedia", "youtube", "who", "start", "Encyclopedia", "facts"]
pattern = "|".join([re.escape(word) for word in words_to_remove])
nouns = re.sub(pattern, "", nouns, flags=re.IGNORECASE)
nouns = re.sub("\s+", " ", nouns).strip()
nouns = nouns.encode('ascii', errors='ignore').decode()
print(nouns)
