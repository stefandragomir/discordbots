

import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer




texts = [
""""
ho ba ca am oprito
aaaaaa
am uitat sa va adaug ca useri
:)))))
apropo trebuie sa va povestesc ce face defapt didi in spate :))))
aduna toate cuvintele care le folosim
vreau sa fac un dictionar de cuvinte usual folosite
ca sale bag in libraria care mia spus @gabriel.manciu nltk
si sa ii dau putina inteligenta
sa poti vorbi aproape natural cu ea
"""
]

df = pd.DataFrame({'sursa': ['wikipedia'], 'text':texts})


cv = CountVectorizer(stop_words='english') 

cv_matrix = cv.fit_transform(df['text'])


df_dtm = pd.DataFrame(cv_matrix.toarray(), index=df['sursa'].values, columns=cv.get_feature_names())

for _entry in df_dtm:

	print(_entry)
