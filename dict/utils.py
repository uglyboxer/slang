import datetime

import pytz
import requests

from xml.etree import ElementTree

from dict.models import Token


def get_new_token(token_obj):
    url = "https://datamarket.accesscontrol.windows.net/v2/OAuth2-13"

    payload = "client_id=563b5fd0-7d43-4e78-a556-2dffe238d83b&client_secret=GPSgnY3kZ%2FsuhtDXvXP6P4T31dThI8Yl721TXypKmF4&grant_type=client_credentials&scope=http%3A%2F%2Fapi.microsofttranslator.com"
    headers = {
        'cache-control': "no-cache",
        'postman-token': "35dbdef3-48f2-f885-6a3d-e6b4a7a5e160",
        'content-type': "application/x-www-form-urlencoded"
        }

    response = requests.request("POST", url, data=payload, headers=headers)
    t = response.json()["access_token"]
    token_obj.token = t
    token_obj.save()
    return t


def get_token():
    """ Check db for still valid token.  If expired, request new one. """
    t = Token.objects.all()[0]
    # now = datetime.datetime.now(pytz.utc)
    # if (now - t.created).total_seconds() > 10:
    #     return t.token
    # else:
    return get_new_token(t)


def get_translation(phrase):
    token = get_token()
    final_token = "Bearer " + token
    headers = {'Authorization': final_token}

    url = "http://api.microsofttranslator.com/v2/Http.svc/Translate?text={}&to=en".format(phrase)

    try:
        translationData = requests.get(url, headers=headers)
        translation = ElementTree.fromstring(translationData.text.encode('utf-8')) 
        return translation.text 

    except OSError:
        pass