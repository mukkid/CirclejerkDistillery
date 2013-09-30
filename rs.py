import requests
import re

def scrape():
    url = "http://www.reddit.com/r/circlejerk"
    return requests.get(url).content

def find_titles():
    return re.findall("<a class=\"title [^>]*>(.*?)</a>",scrape())

def re_quote(deQuote):
    escape_table = {"&quot;" : "\"",
                    "&amp;" : "&",
                    "&lt;" : "<",
                    "&gt;" : ">"}
    for escape_code in escape_table.keys():
        deQuote=deQuote.replace(escape_code,escape_table[escape_code])
    return deQuote

if __name__ == "__main__":
    print re_quote("\n\n".join(find_titles())).encode("utf-8")

