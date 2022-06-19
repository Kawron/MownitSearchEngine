def reducer():
    documents = []
    with open('corpus.txt', 'r', encoding='utf-8') as f:
        corpus = f.read()
        for article in corpus.split('\n\n'):
            name, content = article.split('\n', 1)
            name = name.replace(' ', '_')
            document = {}
            document['name'] = name
            document['content'] = content
            documents.append(document)
    n = len(documents)
    documents = dict(enumerate(documents))
    cnt = 0
    keys = [int(key) for key in documents.keys()]
    for key in keys:
        if cnt % 10 != 0:
            documents.pop(key)
        cnt += 1
    with open('new-corpus.txt', 'w', encoding='utf-8') as f:
        for doc in documents.values():
            f.write(doc['name']+"\n")
            f.write(doc['content']+"\n\n")

reducer()