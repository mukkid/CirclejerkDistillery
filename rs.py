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
content # ---- views the content of post,#\n\n\n"

def re_quote(deQuote):
    escape_table = {"&quot;" : "\"",
                    "&amp;" : "&",
                    "&lt;" : "<",
                    "&gt;" : ">",
                    "&#39;" : "'"}
    for escape_code in escape_table.keys():
        deQuote=deQuote.replace(escape_code,escape_table[escape_code])
    return deQuote

def find_content(s, postid):
    comurl = s.get(url+"/comments/"+postid[3:]).text
    pat = re.compile('<div class=\"md\">([\S\s]*?)</div>')
    fix = re.compile('</?\w+?>')
    print re_quote(re.sub(fix,'',re.findall(pat,comurl)[1]))

def boat_all(s, direct):
    for names in get_data_fullnames(s):
        vote(s, direct, names)
def formatting(s):
    form = re_quote("SPLITMEHERE".join(find_titles(s))).encode("utf-8")
    form = str(form)
    form = re.split('SPLITMEHERE',form)
    form = list(enumerate(form,start=1))
    for n in range(len(form)):
        print str(form[n][0]) + ".  " + str(form[n][1]) + "\n"

def process_input(s, inp):
    if re.match('quit|exit',inp,flags=re.IGNORECASE)!=None:
        exit()
    if re.match('up|upvote',inp,flags=re.IGNORECASE)!=None:
        vote(s,1,get_data_fullnames(s)[int(re.findall('\d+',inp)[0])-1])
        print "upvoted"
    if re.match('down|downvote',inp,flags=re.IGNORECASE)!=None:
        vote(s,-1,get_data_fullnames(s)[int(re.findall('\d+',inp)[0])-1])
        print "downvoted"
    if re.match('neutral|zero|unvote',inp,flags=re.IGNORECASE)!=None:
        vote(s,0,get_data_fullnames(s)[int(re.findall('\d+',inp)[0])-1])
        print "unvoted"
    if re.match('content', inp,flags=re.IGNORECASE)!=None:
        find_content(s,
        get_data_fullnames(s)[int(re.findall('\d+',inp)[0])-1])

    if re.match('help|h|man|manual|h[a+]lp',inp,re.IGNORECASE)!=0:
            help()

if __name__ == "__main__":
    url = url.format(raw_input("SUBREDDIT: "))
    user = requests.session()
    login(user)
    formatting(user)
while True:
    inp = raw_input("COMMAND: ")
    process_input(user,inp)
