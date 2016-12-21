readme.md

# urls
HTML的原文件  
從www.yahoo.com上爬下來的以html結尾的1000頁  
其中mainPage.html是www.yahoo.com首頁  

# dictionaries
html處理後的文件  
用pickle格式dump的  
讀取方法  
```
import pickle
with open(filepath, 'r') as fin:
    d = pickle.load(fin)
```
讀出來d是dict格式  
d['Url'] is url   
d['Title']是文本的title  
d['Content']是文本的內容  
剩下的key是文本中出現的詞  
對應的value是出現的次數  
所有的詞都是小寫後、提取詞乾(stemming)的結果  
```
# cdoe for stemming
from nltk.stem.porter import PorterStemmer 
porter_stemmer = PorterStemmer()
porter_stemmer.stem(word.lower().decode('utf-8'))
```

# tokenize 
相比空格分詞的方法，使用這個的好處是可以去除標點符號。  
```
# code for tokenize
from nltk.tokenize import RegexpTokenizer
tokens = word_tokenize(html_doc)
tokenizer = RegexpTokenizer(r'\w+')
tokenizer.tokenize('Eighty-seven miles to go, yet.  Onward!')
```

# stop word list
一共174個詞  
使用stopwords之後，idf詞表從43936減少到43776個  
