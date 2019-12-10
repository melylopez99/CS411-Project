# -*- coding: utf-8 -*-
"""
Created on Fri Oct 18 12:55:53 2019

@author: Dora
"""

import json, requests

def call_API(search_thing):
    
    url = 'https://api.foursquare.com/v2/venues/explore'

    params = dict(
            client_id='XBMVIFEXCNE42X3JWXMBR1H4SJAMMACGORYNTDPMVVNEZCCE',
            client_secret='JSIL4ZZV0E4WMABHVV1AO5GWDAPUS5P0KQQNHK5JKDDIUNBV',
            v='20180323',
            ll='42.3601,-71.0589',
            query=search_thing,
            limit=10
            )
    resp = requests.get(url=url, params=params)
    data = json.loads(resp.text)
    data_new = data['response']['groups'][0]['items']
    
    final = getPlaces(data_new)
    return final



def getPlaces(data): 
    places_2 = []
    for place in data: 
        name_ = place['venue']['name']
        location = ','.join(place['venue']['location']['formattedAddress'])
        places_2 += [dict(name=name_, address=location)]
    return places_2 
        