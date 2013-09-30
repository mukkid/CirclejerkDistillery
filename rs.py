import requests
import re

def scrape():
    url = "http://www.reddit.com/r/circlejerk"
    return requests.get(url).content

def find_titles():
    return re.findall("<a class=\"title [^>]*>(.*?)</a>",scrape())


if __name__ == "__main__":
    print "\n\n".join(find_titles())

