import random
import requests
import sys
from faker import Faker

"""
Description: Generate list of words from web used for tweets tables
Parameters:
    None

Returns:
    words: Array of encoded words taken from the web
"""
def getListWords():
    # Websites to get words from 
    word_site = "https://www.mit.edu/~ecprice/wordlist.10000"
    word_site2 = "https://svnweb.freebsd.org/csrg/share/dict/words?view=co&content-type=text/plain"
    
    # Extract words from the websites and use it to generate random texts in the tweet tables
    response = requests.get(word_site)
    response2 = requests.get(word_site2)
    words = response.content.splitlines()
    words2 = response2.content.splitlines()
    words.extend(words2)
    return words

"""
Description: Randomly get decoded word from list of words in ASCII format
Parameters:
    WORDS: Array of encoded words taken from the web

Returns:
    decodedWord(string): Word in ASCII format
"""
def getWord(WORDS):
    wordIdx = random.randint(0, len(WORDS)-1)
    decodedWord = WORDS[wordIdx].decode('ASCII')
    return decodedWord

"""
Description: Randomly get decoded word from list of words in ASCII format
Parameters:
    WORDS: Array of encoded words taken from the web

Returns:
    decodedWord(string): Word in ASCII format
"""
def genListName(words):
    numWords = random.randint(1, 3)
    lName = ""
    for i in range(numWords):
        lName += getWord(words)
        if i != numWords-1:
            lName += " "
    return lName

"""
Description: Generate random text for each tweet
Parameters:
    words: Array of encoded words taken from the web
    hashtag_sql: SQL insert statements for the hashtags table
    hashtags: Array of hashtags
    numHashtags(int): Number of hashtags to add to tweet text

Returns:
    randText(string): Tweet text that may or may not include hashtags
    hashtag_sql: New array of insert SQL statements for hashtags table
    hashtags: New array of hashtags
"""
def generateText(words, hashtag_sql, hashtags, numHashtags):
    # Get random number of words to put in tweet text
    numWords = random.randint(7, 35)

    # Get indexes on words to place hashtags at the front of
    hashtagWordIdxes = random.sample(range(0, numWords-1), numHashtags)
    randText = ""
    for i in range(numWords):
        newWord = getWord(words)

        # There are a few words that cannot be retrieved so use davood as default word to avoid error
        if '<' in newWord or '>' in newWord:
            newWord = 'davood'

        # Word will have hashtag added in front
        if i in hashtagWordIdxes:

            # Add new hashtag term to the array of hashtags
            if newWord not in hashtags:
                hashtags.append(newWord)
                hashtag_sql.append(f"INSERT INTO hashtags VALUES ('{newWord}');")
            newWord = "#" + newWord
        randText += newWord
        if i != numWords-1:
            randText += " "
    return randText, hashtag_sql, hashtags

"""
Description: Find a hashtag word then add a row to the mentions table with this hashtag term
Parameters:
    words: Array of encoded words taken from the web
    hashtag_sql: SQL insert statements for the hashtags table
    hashtags: Array of hashtags
    numHashtags(int): Number of hashtags to add to tweet text

Returns:
    hashtagWord(string): Hashtag word to use as a mention term
    0: No hashtag words in tweet text
"""
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

"""
Description: Main function to run program
Parameters:
    None

Returns:
    None
"""
def main():
    words = getListWords()
    fake = Faker()
    if len(sys.argv) > 9:
        # Get command line arguments from user to get number of rows to be added to tables in database
        numUsers = int(sys.argv[1])
        numHashtags = int(sys.argv[2])
        numFollows = int(sys.argv[3])
        numLists = int(sys.argv[4])
        numTweets = int(sys.argv[5])
        numRetweets = int(sys.argv[6])
        numMentions = int(sys.argv[7])
        numIncludes = int(sys.argv[8])

        user_sql = []

        # Generate insert SQL statements for users table
        for i in range(numUsers):
            user_sql.append(f"INSERT INTO users VALUES ({i + 1}, '{fake.name()}', '{fake.email()}', '{fake.city()}', {float(random.randint(-12, 12))});")

        # Extra data that was added to account for John Doe users
        user_sql.append(f"INSERT INTO users VALUES ({numUsers+1}, 'JOHN Doe', 'JohnDoe2@gmail.com', '{fake.city()}', {float(random.randint(-12, 12))});")
        user_sql.append(f"INSERT INTO users VALUES ({numUsers+2}, 'JoHN DoE', 'doey@yahoo.com', '{fake.city()}', {float(random.randint(-12, 12))});")

        tweet_sql = []
        tweetUSRDates = []
        tweetText = {}
        hashtag_sql = []
        hashtags = []

        # Generate insert SQL statements for tweets table
        for i in range(numTweets):
            while True:
                writer = random.randint(1, numUsers+2)
                tdate = fake.date_between(start_date='-1y', end_date='today')

                # Check for unique key violations
                if (writer, tdate) not in tweetUSRDates:
                    break
            tweetUSRDates.append((writer, tdate))
            numHashtags = random.randint(0, 5)
            text, hashtag_sql, hashtags = generateText(words, hashtag_sql, hashtags, numHashtags)
            tweetText[(writer, tdate)] = text

            # Begin choice of adding replies to tweets once 40% of the tweets table is filled
            if i > int((2*numTweets)/5):
                addReply = random.choice([True, False])
                if addReply:
                    randIdx = random.randint(0, len(tweetUSRDates)-1)
                    replyto_w = tweetUSRDates[randIdx][0]
                    replyto_d = tweetUSRDates[randIdx][1]
                    tweet_sql.append(f"INSERT INTO tweets VALUES ({writer}, '{tdate}', '{text}', {replyto_w}, '{replyto_d}');")
                else:
                    tweet_sql.append(f"INSERT INTO tweets VALUES ({writer}, '{tdate}', '{text}', NULL, NULL);")
            
            # By default, tweets will have no replies
            else:
                tweet_sql.append(f"INSERT INTO tweets VALUES ({writer}, '{tdate}', '{text}', NULL, NULL);")

        # Generate insert SQL statements for hashtags table
        for i in range(numHashtags):
            while True:
                term = getWord(words)

                # Check for unique and foreign key violations
                if term not in hashtags and '<' not in term and '>' not in term:
                    break
            hashtags.append(term)
            hashtag_sql.append(f"INSERT INTO hashtags VALUES ('{term}');")

        # Generate insert SQL statements for follows table
        follow_sql = []
        follow_followee = []
        for i in range(numFollows):
            while True:
                flwer = random.randint(1, numUsers+2)
                flwee = random.randint(1, numUsers+2)

                # Check for unique key violations
                if (flwer, flwee) not in follow_followee:
                    break
            follow_followee.append((flwer, flwee))
            start_date = fake.date_between(start_date='-1y', end_date='today')
            follow_sql.append(f"INSERT INTO follows VALUES ({flwer}, {flwee}, '{start_date}');")

        # Generate insert SQL statements for lists table
        list_sql = []
        list_names = []
        for i in range(numLists):
            while True:
                owner = random.randint(1, numUsers+2)
                lname = genListName(words)
                
                # Check for unique key violations
                if lname not in list_names:
                    break
            list_names.append(lname)
            list_sql.append(f"INSERT INTO lists VALUES ('{lname}', {owner});")

        # Generate insert SQL statements for retweets table
        retweet_sql = []
        retweet_list = []
        for i in range(numRetweets):
            while True:
                usr = random.randint(1, numUsers+2)
                randIdx = random.randint(0, len(tweetUSRDates)-1)
                writer = tweetUSRDates[randIdx][0]
                tdate = tweetUSRDates[randIdx][1]

                # Check for unique key violations
                if (usr, writer, tdate) not in retweet_list:
                    break
            retweet_list.append((usr, writer, tdate))
            rdate = fake.date_between(start_date=tdate, end_date='today')
            retweet_sql.append(f"INSERT INTO retweets VALUES ({usr}, {writer}, '{tdate}', '{rdate}');")

        # Generate insert SQL statements for mentions table
        mention_sql = []
        mentions_list = []
        for i in range(numMentions):
            while True:
                randIdx = random.randint(0, len(tweetUSRDates)-1)
                writer = tweetUSRDates[randIdx][0]
                tdate = tweetUSRDates[randIdx][1]
                term = findHashtagWords(tweetText[tweetUSRDates[randIdx]])

                # Check if a hashtag term is returned
                if term != 0:

                    # Check for unique key violations
                    if (writer, tdate, term) not in mentions_list:
                        break
            mentions_list.append((writer, tdate, term))
            mention_sql.append(f"INSERT INTO mentions VALUES ({writer}, '{tdate}', '{term}');")

        # Generate insert SQL statements for mentions table
        include_sql = []
        includes_list = []
        for i in range(numIncludes):
            while True:
                lname = list_names[random.randint(0, len(list_names)-1)]
                member = random.randint(1, numUsers+2)

                # Check for unique key violations
                if (lname, member) not in includes_list:
                    break
            includes_list.append((lname, member))
            include_sql.append(f"INSERT INTO includes VALUES ('{lname}', {member});")

        # Save the SQL statements to a file
        all_sql = user_sql + hashtag_sql + follow_sql + list_sql + tweet_sql + retweet_sql + mention_sql + include_sql
        with open(sys.argv[9], "w") as sql_file:
            sql_file.write("\n".join(all_sql))

        print("SQL statements generated and saved to " + sys.argv[9])
    else:
        print("Not enough command line arguments!!!")

if __name__ == "__main__":
    main()