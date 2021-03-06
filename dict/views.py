import requests
import json
import urllib
import logging
import sys

from lxml import html

from django.shortcuts import render
from django.db.models import Q

from dict.models import Entry

from dict.utils import get_translation


def home_page(request):
    entries = Entry.objects.all().order_by('-queries')[:5]
    return render(request, 'home.html', {'title': 'Slictionary',
                                         'entries': entries})


def search(request):

    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    logger = logging.getLogger(__name__)

    search_term = request.GET['search-term']
    search_term = search_term.lower()
        
    try:
        term_entry = Entry.objects.get(word=search_term)
        term_entry.queries += 1
        term_entry.save()
        return render(request, 'results.html', {'title': 'Slictionary',
                                             'word': term_entry.word,
                                             'definition': term_entry.definition,
                                             'translation': term_entry.translation})

    except:
        # logger.exception('Error in db lookup')
        if not request.GET.get('spanish', ''):
            f = {'term': search_term}
            q = urllib.urlencode(f)
            url = 'http://api.urbandictionary.com/v0/define?' + q
            translation = ""
            try:
                r = requests.get(url)
                data = r.json()
                if data['list']:
                    ret_def = data['list'][0]['definition']
                    entry = Entry(word=search_term, definition=ret_def, response1='',
                                  response2='')
                    entry.save()
                else:
                    ret_def = "No matching results found."
            except requests.exceptions.ConnectionError:
                # logger.exception('Error in urbandict call')
                ret_def = "Connection error, please try again later."

            return render(request, 'results.html', {'title': 'Slictionary',
                                                 'word': search_term, 
                                                 'definition': ret_def,
                                                 'translation': translation})

        else:
            try:
                url_search_term = urllib.quote_plus(search_term)
                page = requests.get(
                    'http://www.asihablamos.com/word/palabra/{}.php?pais=MX'\
                    .format(url_search_term))
                tree = html.fromstring(page.content)
                ret_def = tree.xpath('//div[@class="definicion"]/div[2]/text()')
                if ret_def:
                    definition = ret_def[0]
                    translation = get_translation(ret_def)
                    entry = Entry(word=search_term,
                                  definition=definition,
                                  translation=translation,
                                  response1='',
                                  response2='')
                    entry.save()
                else:
                    definition = "No matching results found."
                    translation = ""
            except requests.exceptions.ConnectionError:
                # logger.exception('Error in asihablamos call')
                pass
            
            return render(request, 'results.html', {'title': 'Slictionary',
                                                 'word': search_term, 
                                                 'definition': definition,
                                                 'translation': translation})
