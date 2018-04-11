# -*- coding: utf-8 -*-
def judge_pure_english(keyword):  
    return all(ord(c) < 128 for c in keyword)  

string = 'ssss frre,.:/?*&^%$#@!()-=_+'
print(judge_pure_english(string))