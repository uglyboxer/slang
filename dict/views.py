import requests
import json

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
    # search_term = request.GET['q']
    search_term = request.POST['search-term']
    search_term = search_term.lower()
        
    # qset = Q()
    # for term in search_term.split():
    #     qset |= Q(name__contains=term)

    # matching_results = Entry.objects.filter(qset)

    # definition = matching_results[0]['definition']

    try:
        term_entry = Entry.objects.get(word=search_term)
        term_entry.queries += 1
        term_entry.save()
        return render(request, 'results.html', {'title': 'Slictionary',
                                             'word': term_entry.word,
                                             'definition': term_entry.definition,
                                             'translation': term_entry.translation})

    except:
        
        if not request.POST.get('spanish', ''):
            url = 'http://api.urbandictionary.com/v0/define?term=%s' % (search_term)

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
                ret_def = "Connection error, please try again later."

            return render(request, 'results.html', {'title': 'Slictionary',
                                                 'word': search_term, 
                                                 'definition': ret_def})

        else:
            try:
                page = requests.get(
                    'http://www.asihablamos.com/word/palabra/{}.php?pais=MX'\
                    .format(search_term))
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
                pass
            
            return render(request, 'results.html', {'title': 'Slictionary',
                                                 'word': search_term, 
                                                 'definition': definition,
                                                 'translation': translation})
