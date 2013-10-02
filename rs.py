import requests
import re
import getpass


user = requests.session()
first_time = True
sraped = ''
post_ids = []
loginurl = "https://ssl.reddit.com/api/login/{}"
baseurl = "http://www.reddit.com/r/{}"
url = ""
voteurl = "http://www.reddit.com/api/vote"
credentials = {
   "op":"login-main",
   "user":raw_input("USERNAME: "),
   "passwd":getpass.getpass("PASSWORD: "),
   "api_type":"json"}

def init(subreddit=raw_input("SUBREDDIT: ")):
    global user
    global url
    global first_time
    global scraped
    global post_ids
    url = baseurl.format(subreddit)
    scraped = scrape(user)
    if first_time:
        login(user)
        first_time = False
    formatting(user)
    post_ids = get_data_fullnames(user)

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
    return re.findall("data-fullname=\"(.*?)\"",scraped)

def get_vote_hash(s):
    return re.findall("\"vote_hash\": \"(.*?)\",",scraped)[0]

def get_mod_hash(s):
    return re.findall("\"modhash\": \"(.*?)\",",scraped)[0]

def find_titles(s):
    return re.findall("<a class=\"title [^>]*>(.*?)</a>",scraped)

def help():
    print "Hello redditer!\n\ncommands:\n\n\t\
quit  -------- exits out of the distillery\n\t\
exit  -------- same as quit\n\t\
upvote # ----- upvotes the post,#\n\t\
up #  -------- same as upvote\n\t\
downvote # --- downvotes the post,#\n\t\
down # ------- same as downvote\n\t\
unvote # ----- unvotes the post,#\n\t\
neutral # ---- same as unvote\n\t\
zero # ------- same as unvote\n\t\
content # ---- views the content of post,#\n\t\
page --------- reprints the page\n\t\
/SUBREDDIT --- changed the subreddit to SUBREDDIT\n\n\n"

def re_quote(deQuote):
    escape_table = {"&quot;" : "\"",
                    "&amp;" : "&",
                    "&lt;" : "<",
                    "&gt;" : ">",
                    "&#39;" : "'"}
    for escape_code in escape_table.keys():
        deQuote=deQuote.replace(escape_code,escape_table[escape_code])
    return deQuote

def get_tags(s):
    tagpat = re.compile('<span \
class=\"domain\">\(<a href=\"[\S\s]*?>(.*?)</a>')
    return re.findall(tagpat,scraped)

def find_content(s, postid):
    comurl = s.get(url+"/comments/"+postid[3:]).text
    pat = re.compile('<div class=\"md\">([\S\s]*?)</div>')
    fix = re.compile('</?\w+?>')
    print re_quote(re.sub(fix,'',re.findall(pat,comurl)[1]))

def boat_all(s, direct):
    for names in post_ids:
        vote(s, direct, names)
def formatting(s):
    form = re_quote("SPLITMEHERE".join(find_titles(s))).encode("utf-8")
    form = str(form)
    form = re.split('SPLITMEHERE',form)
    form = list(enumerate(form,start=1))
    tagged = get_tags(s)
    for n in range(len(form)):
        print (str(form[n][0]).rjust(2) + ".  ["+tagged[n]+"]  "+\
str(form[n][1]).decode('utf-8') + "\n")

def process_input(s, inp):
    global user
    global first_time
    global credentials
    if re.match('quit|exit',inp,flags=re.IGNORECASE)!=None:
        exit()
    elif re.match('up|upvote',inp,flags=re.IGNORECASE)!=None:
        try:
            vote(s,1,post_ids[int(re.findall('\d+',inp)[0])-1])
            print "upvoted"
        except:
            print "you need to log in for that!"
    elif re.match('down|downvote',inp,flags=re.IGNORECASE)!=None:
        try:
            vote(s,-1,post_ids[int(re.findall('\d+',inp)[0])-1])
            print "downvoted"
        except:
            print "you need to log in for that!"
    elif re.match('neutral|zero|unvote',inp,flags=re.IGNORECASE)!=None:
        try:
            vote(s,0,post_ids[int(re.findall('\d+',inp)[0])-1])
            print "unvoted"
        except:
            print "you need to log in for that"
    elif re.match('content', inp,flags=re.IGNORECASE)!=None:
        try:
            find_content(s,
            post_ids[int(re.findall('\d+',inp)[0])-1])
        except:
            print "!!!NOTHING TO SEE HERE!!!"
    elif re.match('/',inp)!=None:
        init(str(re.findall('/\w+$',inp)[0]))
    elif re.match('page',inp,re.IGNORECASE)!=None:
        formatting(s)
    elif re.match('login',inp,re.IGNORECASE)!=None:
        user = requests.session()
        credentials['user'] = raw_input("USERNAME: ")
        credentials['passwd'] = getpass.getpass("PASSWORD: ")
        first_time = True
        init()
    elif re.match('help|h|man|manual|h[a+]lp',inp,re.IGNORECASE)!=0:
        help()

if __name__ == "__main__":
    init()
while True:
    inp = raw_input("COMMAND: ")
    process_input(user,inp)
