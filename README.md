# fasttld
`Fasttld` is a high performance TLD extract module based on a compressed [trie](https://en.wikipedia.org/wiki/Trie) 
with builtin python dict().

![Trie](https://upload.wikimedia.org/wikipedia/commons/b/be/Trie_example.svg)

# Background
The plan of fasttld module is to extract domains from millions lines of DNS data in one time. In the other words, extract
 "www.google.com" into "google.com". Most programmers think it is easy, just run `".".join(domain.split('.')[1::])`. 

But it is wrong ! Think about how to process "www.baidu.com.cn". So we must know what suffixes are.

Thanks to [Mozilla Public Suffix List]((http://www.publicsuffix.org)),it provides us with all suffixes list, including 
some private domains such like 'blogspot.co.uk', 'sinaapp.com'.

# Install
You can install fasttld through PyPI.
```python
pip install fasttld
```
or
```python
git clone https://github.com/jophy/fasttld.git && cd fasttld
python setup.py
```

# Usage
```python
>>> from fasttld import FastTLDExtract
>>> t = FastTLDExtract()
>>> t.extract("www.google.com")
>>> ('www', 'google', 'com', 'google.com')
```

# Comparison
Comparing with the similar modules, eg, [tldextract](https://github.com/john-kurkowski/tldextract) , 
[tld](https://github.com/barseghyanartur/tld). 

Initialize the class one time, calling extract function millions times. Results see below.

 module\case | jophy.com | www.baidu.com.cn|jo.noexist
-------------|-----------|-----------------|----------
fasttld      |    2.93   |       8.68      |  11.50
tldextract   |    3.37   |      11.69      |  11.15
tld          |    1.86   |       9.22      |  12.06

`fasttld` is **five** times faster than the other modules.


