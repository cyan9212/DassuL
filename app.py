"""
Created on Fri Apr 15 17:20:16 2022
@author: seoann
mongoDB add : yckim
"""
from flask import Flask, request, jsonify

from jinja2 import escape
from model import ModelHandler
from transformers import ElectraModel, ElectraTokenizerFast
from transformers import ElectraForSequenceClassification, AdamW
import warnings

import pymongo
from pymongo import MongoClient


myclient = pymongo.MongoClient("mongodb://localhost:27017")
mydb = myclient['lang_db']
mycol = mydb['hate']
# 검색 시 db.hate.find().pretty()

app = Flask (__name__)
handler = ModelHandler()
warnings.filterwarnings('ignore')


@app.route('/')
def chatbot():
    return 'Chat bot Server'


@app.before_first_request
def before_first_request():
    handler.initialize()
    
    

@app.route('/pred', methods = ['POST'])
def pred():
    body = request.get_json()
    text = body['text']
    user_info = body['UserInfo']
    print(text)
    output = handler.handle(text)
    
    #DB 저장
    """
    text와 user info를 전송
    """

    #savetxt = mycol.insert_one({"user_id":user_info , "text" : text})
    #savetxt = mycol.insert_one({"text": text})

    # user_info 및 text 저장
    savetxt = mycol.insert_one({"UserInfo" : user_info, "text": text})

    return jsonify(output)

@app.route('/kakao', methods = ['POST'])
def kakao():
    body = request.get_json()
    userRequest = body['userRequest']
    text = userRequest['utterance']
    user = userRequest['user']
    lang = userRequest['lang']
    if lang != 'kr':
        return jsonify('한글 문장을 입력해주세요.')
    user_info = user['id']
    print(text)
    output = handler.handle(text)
    
    #DB 저장
    """
    text와 user info를 전송
    """

    #savetxt = mycol.insert_one({"user_id":user_info , "text" : text})
    #savetxt = mycol.insert_one({"text": text})

    # user_info 및 text 저장
    #savetxt = mycol.insert_one({"UserInfo" : user_info, "text": text})
    
    return jsonify(output)

    
if __name__ == "__main__":
    app.run(host = '0.0.0.0', port = '5000', debug = True) 
