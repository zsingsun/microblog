import json
import requests
import hashlib
import urllib
import random
from flask_babel import _
from flask import current_app

def translate(text, source_language, dest_language):
    if 'BD_TRANSLATOR_KEY' not in current_app.config or \
            not current_app.config['BD_TRANSLATOR_KEY']:
        return _('Error: the translation service is not configured.')
    
    app_id = current_app.config['BD_TRANSLATOR_APPID']
    secret_key = current_app.config['BD_TRANSLATOR_KEY']

    myurl = 'http://api.fanyi.baidu.com/api/trans/vip/translate'

    fromLang = source_language
    toLang = dest_language
    salt = random.randint(32768, 65536)
    sign = str(app_id) + text + str(salt) + secret_key
    sign = hashlib.md5(sign.encode()).hexdigest()
    
    myurl = myurl + '?appid=' + str(app_id) + '&q=' + urllib.parse.quote(text) + '&from=' + fromLang + '&to=' + toLang + '&salt=' + str(
salt) + '&sign=' + sign

    r = requests.get(myurl)
    if r.status_code != 200:
        return _('Error: the translation service failed.')
    dst = json.loads(r.content.decode('utf-8-sig'))
    return dst['trans_result'][0]['dst']
