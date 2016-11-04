import praw, sys, io
import json
from nltk.corpus import stopwords
from difflib import SequenceMatcher
from fuzzywuzzy import fuzz
import re
import operator



"""
    InitRedditReader()

    Inits the reddit reddit_reader
"""
def InitRedditReader():
    user_agent = ("taagarwal")
    reddit_reader = praw.Reddit(user_agent = user_agent, site_name = 'fsoc')
    return reddit_reader



"""
    RemoveStopWords(words)

    Eliminates stop words from passed text arg
"""
def RemoveStopWords(words):
    filtered_words = []

    for word in words:
        if word not in stopwords.words('english'):
            filtered_words.append(word)

    return filtered_words


"""
    GetSubRedditList(reddit_reader, query)

    Gets the list of associated subreddits
"""
def GetSubRedditList(reddit_reader, query):
    filtered_words = []
    #split query into individual words
    words = query.strip().split(' ')
    #filter out stop words, defined by nltk reader
    words = RemoveStopWords(words)

    subreddit_list = []
    #gather all subreddits
    for word in words:
        subreddit_list = subreddit_list + reddit_reader.search_reddit_names(word)

    return subreddit_list


"""
    SortByRelevanceSubReddits(query, subreddit_list)

    Sorts the subreddits by relevance based on fuzzy string
    matching
"""
def SortByRelevanceSubReddits(query, subreddit_list):
    temp_list = []
    for word in subreddit_list:
        m = fuzz.ratio(query, word.display_name)
        tup = (m, word)
        temp_list.append(tup)

    temp_list = sorted(temp_list, key=lambda tup: tup[1], reverse = True)

    return map(operator.itemgetter(1), temp_list)



"""
    FetchArticles(reddit_reader, sub_reddit_list)

    Fetches list of articles from reddit based on top subreddits
"""
def FetchArticles(reddit_reader, sub_reddit_list):
    result = []
    dict_id= {}

    for subr in sub_reddit_list:

        if(len(result)) > 12:
            break

        submissions = subr.get_top_from_all(limit = None)
        for submission in submissions:
            if(len(result)) > 12:
                break
            #print(submission)
            #print("here")
            if submission.url not in dict_id:
                dict_id[submission.id] = '1'
            else:
                continue
            try:
                result.append({'url':submission.url,'summary':submission.title})
            except:
                x = 1
    return result



"""
    ReturnSearchResults(query)

    Exposed Method to get list of url of relevant articles
"""
def ReturnSearchResults(query):
    reddit_reader = InitRedditReader()

    """Fetching lsit of subreddits """
    sub_reddit_list = GetSubRedditList(reddit_reader, query)
    #print("Raw List")
    #print(sub_reddit_list)
    #print()

    """sorting subreddits by relevance"""
    sub_reddit_list = SortByRelevanceSubReddits(query, sub_reddit_list)
    #print("Sorted by similarity score List")
    #print(sub_reddit_list)
    #print()

    """fetching url of articles"""
    results = FetchArticles(reddit_reader, sub_reddit_list)
    #print("Raw Results")
    #print(results)
    #print()

    """Dumping to file in json format"""
    data_file = open('full_listing.nb', 'w')

    json.dump(results, data_file)
    data_file.close()



def test():
    ReturnSearchResults("Fuck Trump")

"""test()"""















"""
    submissions = subreddit.get_rising(limit = None)
    for submission in submissions:
        if submission.id not in dict_id:
            dict_id[submission.id] = '1'
        else:
            continue

        try:
            print(submission.title)
            summary_file.write(submission.title+'\n')
            url_lsit.append({'url':submission.url,'summary':submission.title})
        except:
            x = 1


    submissions = subreddit.get_hot(limit = None)
    for submission in submissions:
        if submission.id not in dict_id:
            dict_id[submission.id] = '1'
        else:
            continue

        try:
            print(submission.title)
            summary_file.write(submission.title+'\n')
            url_lsit.append({'url':submission.url,'summary':submission.title})
        except:
            x = 1


    submissions = subreddit.get_top_from_all(limit = None)
    for submission in submissions:
        if submission.id not in dict_id:
            dict_id[submission.id] = '1'
        else:
            continue

        try:
            print(submission.title)
            summary_file.write(submission.title+'\n')
            url_lsit.append({'url':submission.url,'summary':submission.title})
        except:
            x = 1
"""
