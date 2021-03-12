import json

import requests
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.throttling import UserRateThrottle
from rest_framework.views import APIView
from django.core.paginator import Paginator
from django.core.cache import cache
import hashlib

class BasicHtmlView(APIView):
    throttle_classes = [UserRateThrottle]

    def get(self, request):
        try:
            return render(request, 'home/index.html')
        except Exception as e:
            print(str(e))


class StackOverflowForm(APIView):

    def get(self, request):
        params = {}
        keys = request.GET.keys()

        for k in keys:
            if k == 'django_page':
                continue
            params[k] = request.GET[k]
        # response = requests.get(base_url, params=params)
        cache_key = hashlib.sha1(json.dumps(params,sort_keys=True).encode()).hexdigest()
        user_data = cache.get(cache_key)
        print ('user_data')
        if not user_data:
            user_data = self.call_api(params)
            cache.set(cache_key,
                    user_data,
                    timeout=900)
        
        paginator = Paginator(user_data['items'],10)
        page_val = request.GET.get('django_page',1)

        try:
            content = paginator.page(page_val)
        except Exception as e:
            content = paginator.page(1)
        except Exception as e:
            content = paginator.page(paginator.num_pages)
        return render(request, 'home/display.html', {'content': content})
    
    def call_api(self, params):
        base_url = 'https://api.stackexchange.com/2.2/questions?'
        params['site'] = 'stackoverflow'
        response = requests.get(base_url, params=params)
        print ('he;ll;')
        return response.json()
