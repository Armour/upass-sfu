
# coding: utf-8

# In[48]:


import requests
import json
from lxml import html, etree

r = requests.Session()
# r.headers.update({'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'})

r1 = r.get('https://upassbc.translink.ca/')
# print(r1.status_code)
# print(r1.cookies)

r2 = r.post('https://upassbc.translink.ca/', data={'PsiId':'sfu'})
# print(r2.status_code)
# print(r2.cookies)
# for history in r2.history:
#     print(history)
#     print(history.url)
tree = html.fromstring(r2.content)
form = tree.find('.//form[@class="signin-form"]')
hiddenFields = form.findall('.//input[@type="hidden"]')
with open('config.json') as config:    
    data = json.load(config)
for hiddenField in hiddenFields:
    data[hiddenField.name] = hiddenField.value
# print(r.cookies)

r3 = r.post('https://cas.sfu.ca' + form.action, data=data)
# print(r3.status_code)
# print(r3.cookies)
# for history in r3.history:
#     print(history)
#     print(history.url)
tree = html.fromstring(r3.content)
form = tree.find('.//form')
fields = form.findall('.//input')
data = {}
for field in fields:
    data[field.name] = field.value

r4 = r.post('https://upassadfs.translink.ca/adfs/ls/', data=data)
# print(r4.status_code)
# print(r4.cookies)
# for history in r4.history:
#     print(history)
#     print(history.url)
tree = html.fromstring(r4.content)
form = tree.find('.//form')
fields = form.findall('.//input')
data = {}
for field in fields:
    data[field.name] = field.value

r5 = r.post('https://upassbc.translink.ca/fs/', data=data)
# print(r5.status_code)
# print(r5.cookies)
# for history in r5.history:
#     print(history)
#     print(history.url)
print(r5.text)


