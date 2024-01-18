import random
import requests
from faker import Faker

def getListWords():
    word_site = "https://www.mit.edu/~ecprice/wordlist.10000"
    word_site2 = "https://svnweb.freebsd.org/csrg/share/dict/words?view=co&content-type=text/plain"
    response = requests.get(word_site)
    response2 = requests.get(word_site2)
    words = response.content.splitlines()
    words2 = response2.content.splitlines()
    words.extend(words2)
    return words

def getWord(WORDS):
    wordIdx = random.randint(0, len(WORDS)-1)
    decodedWord = WORDS[wordIdx].decode('ASCII')
    return decodedWord

def genListName(words):
    numWords = random.randint(1, 3)
    lName = ""
    for i in range(numWords):
        lName += getWord(words)
        if i != numWords-1:
            lName += " "
    return lName

def generateText(words, hashtag_sql, hashtags, numHashtags):
    numWords = random.randint(7, 35)
    hashtagWordIdxes = random.sample(range(0, numWords-1), numHashtags)
    randText = ""
    for i in range(numWords):
        newWord = getWord(words)
        if '<' in newWord or '>' in newWord:
            newWord = 'davood'
        if i in hashtagWordIdxes:
            if newWord not in hashtags:
                hashtags.append(newWord)
                hashtag_sql.append(f"INSERT INTO hashtags VALUES ('{newWord}');")
            newWord = "#" + newWord
        randText += newWord
        if i != numWords-1:
            randText += " "
    return randText, hashtag_sql, hashtags

def findHashtagWords(text):
    splitText = text.split()
    hashtagWords = []
    for word in splitText:
        if word.startswith("#"):
            hashtagWords.append(word[1:])
    if len(hashtagWords) > 0:
        randIdx = random.randint(0, len(hashtagWords)-1)
        hashtagWord = hashtagWords[randIdx]
        return hashtagWord
    else:
        return 0
    


words = getListWords()

fake = Faker()

numUsers = int(input("Enter the number of rows for the users table: "))
numHashtags = int(input("Enter the number of additional rows for the hashtags table: "))
numFollows = int(input("Enter the number of rows for the follows table: "))
numLists = int(input("Enter the number of rows for the lists table: "))
numTweets = int(input("Enter the number of rows for the tweets table: "))
numRetweets = int(input("Enter the number of rows for the retweets table: "))
numMentions = int(input("Enter the number of rows for the mentions table: "))
numIncludes = int(input("Enter the number of rows for the includes table: "))

# Generate SQL for inserting users
user_sql = []
usr_att = []
for i in range(numUsers):
    usr_att.append(i+1)
    user_sql.append(f"INSERT INTO users VALUES ({i + 1}, '{fake.name()}', '{fake.email()}', '{fake.city()}', {float(random.randint(-12, 12))});")
user_sql.append(f"INSERT INTO users VALUES ({numUsers+1}, 'JOHN Doe', 'JohnDoe2@gmail.com', '{fake.city()}', {float(random.randint(-12, 12))});")
user_sql.append(f"INSERT INTO users VALUES ({numUsers+2}, 'JoHN DoE', 'doey@yahoo.com', '{fake.city()}', {float(random.randint(-12, 12))});")

# Generate SQL for inserting tweets
tweet_sql = []
tweetUSRDates = []
tweetText = {}
hashtag_sql = []
hashtags = []
for i in range(numTweets):
    while True:
        writer = random.randint(1, numUsers+2)
        tdate = fake.date_between(start_date='-1y', end_date='today')
        if writer in usr_att:
            if (writer, tdate) not in tweetUSRDates:
                break
    tweetUSRDates.append((writer, tdate))
    numHashtags = random.randint(0, 5)
    text, hashtag_sql, hashtags = generateText(words, hashtag_sql, hashtags, numHashtags)
    tweetText[(writer, tdate)] = text
    if i > int((2*numTweets)/5):
        addReply = random.choice([True, False])
        if addReply:
            while True:
                randIdx = random.randint(0, len(tweetUSRDates)-1)
                replyto_w = tweetUSRDates[randIdx][0]
                replyto_d = tweetUSRDates[randIdx][1]
                if replyto_w in usr_att:
                    tweet_sql.append(f"INSERT INTO tweets VALUES ({writer}, '{tdate}', '{text}', {replyto_w}, '{replyto_d}');")
                    break
        else:
            tweet_sql.append(f"INSERT INTO tweets VALUES ({writer}, '{tdate}', '{text}', NULL, NULL);")
    else:
        tweet_sql.append(f"INSERT INTO tweets VALUES ({writer}, '{tdate}', '{text}', NULL, NULL);")

# Generate SQL for inserting additional hashtags
for i in range(numHashtags):
    while True:
        term = getWord(words)
        if term not in hashtags and '<' not in term and '>' not in term:
            break
    hashtags.append(term)
    hashtag_sql.append(f"INSERT INTO hashtags VALUES ('{term}');")

# Generate SQL for inserting follows
follow_sql = []
follow_followee = []
for i in range(numFollows):
    while True:
        flwer = random.randint(1, numUsers+2)
        flwee = random.randint(1, numUsers+2)
        if (flwer, flwee) not in follow_followee:
            break
    follow_followee.append((flwer, flwee))
    start_date = fake.date_between(start_date='-1y', end_date='today')
    follow_sql.append(f"INSERT INTO follows VALUES ({flwer}, {flwee}, '{start_date}');")

# Generate SQL for inserting lists
list_sql = []
list_names = []
for i in range(numLists):
    while True:
        owner = random.randint(1, numUsers+2)
        lname = genListName(words)
        if lname not in list_names:
            break
    list_names.append(lname)
    list_sql.append(f"INSERT INTO lists VALUES ('{lname}', {owner});")

# Generate SQL for inserting retweets
retweet_sql = []
retweet_list = []
for i in range(numRetweets):
    while True:
        usr = random.randint(1, numUsers+2)
        randIdx = random.randint(0, len(tweetUSRDates)-1)
        writer = tweetUSRDates[randIdx][0]
        tdate = tweetUSRDates[randIdx][1]
        if (usr, writer, tdate) not in retweet_list:
            break
    retweet_list.append((usr, writer, tdate))
    rdate = fake.date_between(start_date=tdate, end_date='today')
    retweet_sql.append(f"INSERT INTO retweets VALUES ({usr}, {writer}, '{tdate}', '{rdate}');")

# Generate SQL for inserting mentions
mention_sql = []
mentions_list = []
for i in range(numMentions):
    while True:
        randIdx = random.randint(0, len(tweetUSRDates)-1)
        writer = tweetUSRDates[randIdx][0]
        tdate = tweetUSRDates[randIdx][1]
        term = findHashtagWords(tweetText[tweetUSRDates[randIdx]])
        if term != 0:
            if (writer, tdate, term) not in mentions_list:
                break
    mentions_list.append((writer, tdate, term))
    mention_sql.append(f"INSERT INTO mentions VALUES ({writer}, '{tdate}', '{term}');")

# Generate SQL for inserting includes
include_sql = []
includes_list = []
for i in range(numIncludes):
    while True:
        lname = list_names[random.randint(0, len(list_names)-1)]
        member = random.randint(1, numUsers+2)
        if (lname, member) not in includes_list:
            break
    includes_list.append((lname, member))
    include_sql.append(f"INSERT INTO includes VALUES ('{lname}', {member});")
all_sql = user_sql + hashtag_sql + follow_sql + list_sql + tweet_sql + retweet_sql + mention_sql + include_sql

# Save the SQL statements to a file
with open("insert_statements.sql", "w") as sql_file:
    sql_file.write("\n".join(all_sql))

print("SQL statements generated and saved to 'insert_statements.sql'.")
