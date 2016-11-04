import json
import os
import re
from bs4 import BeautifulSoup
import urllib2
import sys
from f_scrape import ReturnSearchResults

"""
    GetArticleText(string query)

    Takes in a valid string query and returns a list of dictionary of associated
    articles, url and summaries

    Dictionary has keys os url, summary and text for respective fields

"""
def GetArticleText(query):
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
            return result


def test():
    result = GetArticleText("Fuck Trump")
    print(result)

test()
