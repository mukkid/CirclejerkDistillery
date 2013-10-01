import requests
import re
import getpass

loginurl = "https://ssl.reddit.com/api/login/{}"
url = "http://www.reddit.com/r/{}"
voteurl = "http://www.reddit.com/api/vote"
credentials = {
   "op":"login-main",
   "user":raw_input("USERNAME: "),
   "passwd":getpass.getpass("PASSWORD: "),
   "api_type":"json"}

def scrape(s):
    return s.get(url).text

def login(s):
    r = s.post(loginurl.format(credentials["user"]),
            params=credentials)
    print r.json()

def vote(s, direct, iden):
    vote_data = {
       "id":iden,
       "dir":direct,
       "vh":get_vote_hash(s),
       "r":re.findall("/r/(.*)$",url)[0],
       "uh":get_mod_hash(s)}
    return s.post(voteurl, params=vote_data)

def get_data_fullnames(s):
    return re.findall("data-fullname=\"(.*?)\"",scrape(s))

def get_vote_hash(s):
    return re.findall("\"vote_hash\": \"(.*?)\",",scrape(s))[0]

def get_mod_hash(s):
    return re.findall("\"modhash\": \"(.*?)\",",scrape(s))[0]

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

def boat_all(s, direct):
    for names in get_data_fullnames(s):
        vote(s, direct, names)

if __name__ == "__main__":
    url = url.format(raw_input("SUBREDDIT: "))
    user = requests.session()
    login(user)
    #boat_all(user, 1)
    vote(user, 1, get_data_fullnames(user)[0])
    print re_quote("\n\n".join(find_titles(user))).encode("utf-8")

