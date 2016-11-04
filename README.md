### fsociety
Hackathon project at VMware: Smart Lorem ipsum generator

## Reddit Scraper

*Usage*

    from f_aggr import GetArticleText

>GetArticleText(query) : Takes in string query and returns
result as a list of dictionaries with keys url, summary and text.
This text is converted to pure ASCII and all unicode (including emojis) are filtered out.
