#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/6/13 11:20
# @Author  : Yizheng Dai
# @Email   : 387942239@qq.com
# @File    : test1.py
# import spacy
#
# nlp = spacy.load("en_core_web_sm")
text = "Complete Response to Pembrolizumab in Advanced Colon Cancer Harboring Somatic POLE F367S Mutation with Microsatellite Stability Status: A Case Study. "
# tokens = nlp(text)
# offset_mapping = []
# init_start = 0
# new_text = ""
# for token in tokens:
#     index = 0
#     while True:
#         if (new_text + " " * index + token.text) in text:
#             new_text += " " * index + token.text
#             break
#         if len(new_text + " " * index + token.text) > len(text):
#             raise ValueError
#         index += 1
#     assert text[init_start+index: len(new_text)] == token.text, \
#         "offset_mapping is not aligned, token: %s, position:%d, %d" % (token.text, init_start+index, len(new_text))
#     offset_mapping.append((init_start, len(new_text)))
#     init_start = len(new_text)
# print(offset_mapping)
from liyi_cute.processor.tokenizers.word_tokenizer import WordTokenizeFast

tokenizer = WordTokenizeFast(spacy_model="en_core_web_sm")
t = tokenizer.tokenize(text=text)
print(t)