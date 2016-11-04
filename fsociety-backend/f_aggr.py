import json
import os
import re
from bs4 import BeautifulSoup
import urllib2
import sys
from f_scrape import ReturnSearchResults


"""
    breakintoparas(num_para)

    Break into number of paragraphs passed
"""
def breakintoparas(num_paras, raw_text):
    para_list = []
    para_text = ''
    words  = raw_text.strip().split()
    words_in_a_para = len(words)/num_paras
    count = 0

    for word in words:
        if len(para_list) == num_paras:
            break
        #print(word)
        para_text = para_text + ' ' + word
        #print(para_text)
        count = count + 1
        if count >= words_in_a_para:
            para_list.append(para_text)
            para_text = ''
            count = 0
        else:
            continue

    return para_list

"""
    GetArticleText(string query)

    Takes in a valid string query and returns a list of dictionary of associated
    articles, url and summaries

    Dictionary has keys os url, summary and text for respective fields

"""
def GetArticleText(query, para_count):
    """Fire the reddit engine to retrieve url"""
    ReturnSearchResults(query)
    result = []

    """Loop over genrated file by reddit engine"""
    for filename in os.listdir('.'):
        if filename.endswith('.nb'):
            f = open(filename)
            listing = json.load(f)
            count = 0

            """
                For each url listed in file.nb,
                extract article text
            """
            for item in listing:
                try:
                    page = urllib2.urlopen(item['url']).read()
                    parsed_html = BeautifulSoup(page, 'html.parser')

                    content = []
                    for part in parsed_html.body.findAll('p'):
                        content.append(part.text)

                    if len(content) != 0:
                        """
                            Text claening involves removal of white spaces and
                            new line characters. We also remove all special uniocde characters
                            by converting it to ASCII.
                        """
                        text = ' '.join(content)
                        text = re.sub(' +',' ',text)
                        text = re.sub('\n',' ',text)
                        text = text.encode('ascii','ignore')
                        result.append({'url':item['url'],'summary':item['summary'].strip(), 'text':text})

                except:
                    count += 1

            f.close()

            #result has a list of dicts
            raw_text = ""
            for dicts in result:
                raw_text = raw_text + dicts['text']

            para_list = breakintoparas(para_count, raw_text)


            return para_list


def test():
    para_list = GetArticleText("Fuck Trump", 5)
    print(para_list)

#test()
