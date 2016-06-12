import requests
import json

from django.shortcuts import render
from django.db.models import Q

from dict.models import Entry


def home_page(request):
    entries = Entry.objects.all().order_by('-queries')[:5]
    return render(request, 'home.html', {'title': 'Slictionary',
                                         'entries': entries})


def search(request):
    search_term = request.GET['q']
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
                                             'definition': term_entry.definition})

    except:
        
        url = 'http://api.urbandictionary.com/v0/define?term=%s' % (search_term)

        r = requests.get(url)
        data = r.json()
        ret_def = data['list'][0]['definition']
        entry = Entry(word=search_term, definition=ret_def, response1='',
                      response2='')
        entry.save()
        return render(request, 'home.html', {'title': 'Slictionary',
                                             'word': search_term, 
                                             'definition': ret_def})
