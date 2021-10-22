import nltk



_text = """
ho ba ca am oprito
aaaaaa
am uitat sa va adaug ca useri
:)))))
apropo trebuie sa va povestesc ce face defapt didi in spate :))))
aduna toate cuvintele care le folosim
yvreau sa fac un dictionar de cuvinte usual folosite
ca sale bag in libraria care mia spus @gabriel.manciu nltk
si sa ii dau putina inteligenta
sa poti vorbi aproape natural cu ea
"""

_tokens = nltk.tokenize.word_tokenize(_text)

print(_tokens)
print()
print()

_tags = nltk.pos_tag(_tokens)

print(_tags)