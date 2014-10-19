from django.views import generic
from croplet_demo import settings
from models import AccessToken
from mixins import LoggedInMixin
from urllib2 import urlopen, Request, HTTPError
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
import requests
import json
import re


class Home(generic.TemplateView):
    template_name = "base.html"

    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data(**kwargs)
        context['topbar'] = 'home'
        return context

class MapView(LoggedInMixin, generic.TemplateView):
    template_name = "map.html"

    def get_centroid_for_field(self, client_id, field_id):
        req = Request('http://localhost:8000/api/v3/cropfield/%s/centroid?client_id=%s' % (field_id, client_id))
        req.add_header('Authorization', 'Bearer %s' % self.request.user.access_token.access_token)
        req.add_header('Accept', 'application/json')
        response = urlopen(req)
        return json.loads(response.read())

    def get_data_from_gps(self, lattitude, longitude):
        raw = requests.get('http://gps.buienradar.nl/getrr.php?lat=%s&lon=%s' % (lattitude, longitude))
        m = re.findall('\d+\|\d+\:\d+', raw.content)
        returnvalues = []
        for result in m:
            data, time = result.split('|')
            returnvalues.append({"time": time,
                                 "data": 10**((int(data)-109)/32.0)})
        return returnvalues


    def get_context_data(self, **kwargs):
        context = super(MapView, self).get_context_data(**kwargs)
        client_id = settings.CROPLET_API_CLIENT_ID
        context['client_secret'] = settings.CROPLET_SECRET_API_KEY
        context['client_id'] = client_id
        tokens = AccessToken.objects.filter(user=self.request.user)[:1]
        token = tokens[0].access_token if tokens else ""
        req = Request('http://localhost:8000/api/v3/cropfield/?client_id=%s' % client_id)
        req.add_header('Authorization', 'Bearer %s' % token)
        req.add_header('Accept', 'application/json')

        try:
            response = urlopen(req)
            response = json.loads(response.read())
            data = []
            for cropfield in response:
                print cropfield.get('_id')
                centroid = self.get_centroid_for_field(client_id, cropfield.get('_id'))
                borders = [[x, y] for y, x in cropfield.get('border')[0]]
                #borders = cropfield.get('border')[0]
                cropfield['border'] = borders
                cropfield['pointer'] = {"x": centroid.get('centroid')[0], "y": centroid.get('centroid')[1]}
                cropfield['rainfall'] = self.get_data_from_gps(centroid.get('centroid')[0], centroid.get('centroid')[1])
                cropfield['id'] = cropfield['_id']
                data.append(cropfield)
            context['cropfields'] = data
        except HTTPError as e:
            context['error'] = e
            response = e
        context['topbar'] = 'map'
        context['response'] = response
        print response
        return context

@login_required
def callback(request):
    client_id = settings.CROPLET_API_CLIENT_ID
    client_secret = settings.CROPLET_SECRET_API_KEY
    error = request.GET.get('error')
    auth_code = request.GET.get('code')
    if (error != None):
        pass
    elif (auth_code != None):
        data = {'grant_type':'authorization_code',
                   'code':auth_code,
                   'client_id': client_id,
                   'client_secret': client_secret}
        response = requests.post(
                        'http://localhost:8000/oauth2/access_token/', data)
        response = json.loads(response.text)

        if hasattr(request.user, "access_token"):
            AccessToken.objects.get(user=request.user).delete()
        token = AccessToken(user=request.user)
        access_token = response.get('access_token')
        if access_token:
            accessToken = AccessToken(user=request.user, access_token=access_token)
            accessToken.save()
            request.user.access_token = token
            request.user.save()
    return redirect(reverse('map'))

def convert_response_to_json(response):
    return json.loads(response.read())