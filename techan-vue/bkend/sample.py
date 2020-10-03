import sys
import json

f = open('test.json', 'r')
#print(1)
json_dict = json.load(f)
#print(2)

dat1=json_dict['stock_num']

def sum(a):
    return a+3

print(dat1) #printの内容をpython-shellに返却する