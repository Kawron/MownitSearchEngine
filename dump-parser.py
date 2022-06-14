import re
import wikipedia
import json
import random

def get_article_titles(file_path, maxLines):
    titles = []
    titlesNoTags = []

    file = open(file_path, encoding='utf-8', mode='r')

    numOfLines = 0
    for line in file:
        if '<title>' in line:
            titles.append(line)
        numOfLines += 1
        if numOfLines > maxLines:
            break
    
    for title in titles:
        title = title.replace("<title>", "")
        title = title.replace("</title>", "")
        title = title.replace("\n", "")
        titlesNoTags.append(title)
    
    # print(titlesNoTags)
    random.shuffle(titlesNoTags)
    return titlesNoTags

def save_article_to_json(titles, dirpath):
    cnt = 0
    for title in titles:
        cnt += 1
        print(cnt)
        try:
            dictionary = {}
            wikiPage = wikipedia.page(title)
            dictionary["title"] = title
            dictionary["url"] = wikiPage.url
            dictionary["content"] = wikiPage.content

            #save file
            jsonObject = json.dumps(dictionary, indent = 4)
            out = open(f"{dirpath}/{title}.json", encoding='utf-8', mode='w')
            out.write(jsonObject)
            out.close()
        except Exception as e:
            print(e)