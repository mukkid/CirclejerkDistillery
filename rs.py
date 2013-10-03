import requests
import re
import getpass

page = 1
user = requests.session()
first_time = True
logged_in = False
comment_number = 10
sraped = ''
post_ids = []
loginurl = "https://ssl.reddit.com/api/login/{}"
logouturl = "http://www.reddit.com/logout"
checkurl = "http://www.reddit.com/api/username_available.json"
baseurl = "http://www.reddit.com/r/{}"
url = ""
subreddit = ''
voteurl = "http://www.reddit.com/api/vote"
credentials = {
   "op":"login-main",
   "user":raw_input("USERNAME: "),
   "passwd":getpass.getpass("PASSWORD: "),
   "api_type":"json"}

def init(sub=raw_input("SUBREDDIT: ")):
    global use
    global url
    global first_time
    global scraped
    global post_ids
    subreddit = sub
    url = baseurl.format(sub)
    scraped = scrape(user)
    if first_time:
        login(user)
        first_time = False
    #print user.get('http://www.reddit.com/api/me.json').text
    formatting(user)
    post_ids = get_data_fullnames(user)

def scrape(s):
    return s.get(url).text

def check_user(user):
    outdata = {"user": user}
    r = requests.get(checkurl, params=outdata)
    return r.text == "false"

def login(s):
    global logged_in
    if logged_in: logout(s)
    if credentials['user'] \
        and check_user(credentials['user']) \
        and credentials['passwd']:
        r = s.post(loginurl.format(credentials["user"]),
                params=credentials)
        try:
            error = r.json()['json']['errors']
            if error:
                print "\n".join(["{0}: {1}".format(i[0], i[1]) for i in error])
                logged_in = Flase
                return False
            else:
                logged_in = True
                return True
        except:
            logged_in = False
            return False
    else:
        logged_in = False
        return False

def logout(s):
    outdata = {
            'uh':get_mod_hash(s),
            'top':"off",
            'dest':'/r/'+subreddit}
    r = s.post(logouturl,params=outdata)
    logged_in = False

def vote(s, direct, iden):
    if not logged_in: return False
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
    mhash = s.get('http://www.reddit.com/api/me.json')
    try:
        return mhash.json()['data']['modhash']
    except:
        return ""

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
comments # --- views the comments of post,#\n\t\
comnum # ----- changes number of comments viewed by comments to #\n\t\
page --------- reprints the page\n\t\
next --------- goes to the next page in this subreddit\n\t\
prev --------- goes to the previous page in this subreddit\n\t\
previous ----- same as prev\n\t\
back --------- same as prev\n\t\
login -------- prompts the user to login\n\t\
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

def find_comments(s, postid):
    global post_ids
    global url
    url = re.sub('/\?count=.+','',url)
    comurl = s.get(url+"/comments/"+post_ids[postid][3:]).text
    pat = re.compile('<div class=\"md\">([\S\s]*?)</div>')
    fix = re.compile('</?\w+?>')
    for n in range(2,comment_number):
        print re_quote(re.sub(fix,'',str(re.findall(pat,comurl)[n])))

def find_content(s, postid):
    global post_ids
    global url
    url = re.sub('/\?count=.+','',url)
    comurl = s.get(url+"/comments/"+post_ids[postid][3:]).text
    pat = re.compile('<div class=\"md\">([\S\s]*?)</div>')
    fix = re.compile('</?\w+?>')
    print re_quote(re.sub(fix,'',str(re.findall(pat,comurl)[1])))

def boat_all(s, direct):
    for names in post_ids:
        vote(s, direct, names)
def formatting(s):
    global page
    try:
        form = re_quote("SPLITMEHERE".\
join(find_titles(s))).encode("utf-8")
        form = str(form)
        form = re.split('SPLITMEHERE',form)
        form = list(enumerate(form,start=1))
        tagged = get_tags(s)
        for n in range(len(form)):
            print (str(form[n][0]+25*\
(page-1)).rjust(2)+".  ["+tagged[n]+"]  "+\
str(form[n][1]).decode('utf-8') + "\n")
    except:
        print "nope"

def move_back():
    global post_ids
    global url
    global page
    global scraped
    url = re.findall\
('nextprev\">view more:&#32;<a href=\"([\S\s]*?)\"',scraped)[0]
    scraped = scrape(user)
    post_ids = get_data_fullnames(user)
    page = page - 1
    formatting(user)

def move_pages():
    global post_ids
    global url
    global page
    global scraped
    url = url+'/?count=1&after='+post_ids[len(post_ids)-1]
    scraped = scrape(user)
    post_ids = get_data_fullnames(user)
    page = page+1
    formatting(user)

def set_comment_number(number):
    global comment_number
    comment_number = number+2

def process_input(s, inp):
    global user
    global first_time
    global credentials
    global page
    if re.match('quit|exit',inp,flags=re.IGNORECASE)!=None:
        exit()
    elif re.match('up|upvote',inp,flags=re.IGNORECASE)!=None:
            vote(user,1,post_ids[int(re.findall('\d+',inp)[0])-1])
            print "upvoted"
    elif re.match('down|downvote',inp,flags=re.IGNORECASE)!=None:
            vote(user,-1,post_ids[int(re.findall('\d+',inp)[0])-1])
            print "downvoted"
    elif re.match('neutral|zero|unvote',inp,flags=re.IGNORECASE)!=None:
            vote(user,0,post_ids[int(re.findall('\d+',inp)[0])-1])
            print "unvoted"
    elif re.match('content', inp,flags=re.IGNORECASE)!=None:
        # try:
            find_content(s,int(re.findall('\d+',inp)[0])-25*(page-1)-1)
            # except:
           # print "!!!NOTHING TO SEE HERE!!!"
    elif re.match('comments', inp,flags=re.IGNORECASE)!=None:
        # try:
        find_comments(s,int(re.findall('\d+',inp)[0])-25*(page-1)-1)
            # except:
           # print "!!!NOTHING TO SEE HERE!!!"
    elif re.match('/',inp)!=None:
        try:
            init(str(re.findall('/\w+$',inp)[0]))
        except:
            print "COULDN'T FIND THAT SUBREDDIT"
    elif re.match('page',inp,re.IGNORECASE)!=None:
        formatting(s)
    elif re.match('next',inp,re.IGNORECASE)!=None:
        move_pages()
    elif re.match('prev|back|previous',inp,re.IGNORECASE)!=None:
        move_back()
    elif re.match('comnum',inp,re.IGNORECASE)!=None:
        set_comment_number(int(re.findall('\d+',inp)[0]))
    elif re.match('login',inp,re.IGNORECASE)!=None:
        credentials['user'] = raw_input("USERNAME: ")
        credentials['passwd'] = getpass.getpass("PASSWORD: ")
        login(user)
    elif re.match('help|h|man|manual|h[a+]lp',inp,re.IGNORECASE)!=0:
        help()

if __name__ == "__main__":
    init()
    while True:
        inp = raw_input("COMMAND: ")
        process_input(user,inp)
