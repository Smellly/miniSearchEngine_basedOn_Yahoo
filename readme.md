readme.md

# 運行順序
1. 爬取文件
```python yahoo.py```

2. 提取文本內容
```python htmlProcess.py```

3. 計算idf
```python idf.py```

4. 建立單詞和文件編碼
```
python word_file_index/word_file_index.py
```

5. 儲存詞表的 idf
詞表每個詞的idf
```
python word_idf_array/word_idf_array.py
```
6. 儲存文章列表的 tf
計算每篇文章的tf，並存儲
```
python file_word_tf_array/file_word_tf_array.py
```

7. 計算 tf-idf
```
python tf_idf_array/tf_idf_array.py
```

8. 建立倒排表
```
python inverted_list/inverted_list.py
```

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
d['Raw']是文本的原始內容，字符串的形式    
d['Content']是文本的分詞後的內容，是列表的形式，列表內是每個分好的詞    
d['Length']是文本去除停用詞後的詞數  
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

# htmlProcess.py
對html文本內容進行提取，  
分詞  
stemming  
最後統計詞頻  

# idf.py  
統計了詞在所有文檔中出現的次數  

# numpy 的存取
利用这种方法，保存文件的后缀名字一定会被置为.npy   
```
numpy.save("filename.npy",a)
```
这种格式最好只用```a = numpy.load("filename")```来读取。