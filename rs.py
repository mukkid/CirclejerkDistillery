import requests
import re
import getpass

credentials = {
   "op":"login-main",
   "user":raw_input("USERNAME: "),
   "passwd":getpass.getpass("PASSWORD: "),
   "api_type":"json"}

def scrape(s):
    url = "http://www.reddit.com/r/circlejerk"
    return s.get(url).text

def login(s):
    loginurl = "https://ssl.reddit.com/api/login/{}"
    r = s.post(loginurl.format(credentials["user"]),
            params=credentials)
    print r.json()

def find_titles(s):
    return re.findall("<a class=\"title [^>]*>(.*?)</a>",scrape(s))

def re_quote(deQuote):
    escape_table = {"&quot;" : "\"",
                    "&amp;" : "&",
                    "&lt;" : "<",
                    "&gt;" : ">"}
    for escape_code in escape_table.keys():
        deQuote=deQuote.replace(escape_code,escape_table[escape_code])
    return deQuote

if __name__ == "__main__":
    user = requests.session()
    login(user)
    print re_quote("\n\n".join(find_titles(user))).encode("utf-8")

