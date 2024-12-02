from django.shortcuts import render
from django.http import HttpRequest , HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import http.client
# Create your views here.
# def career_test_view(request:HttpRequest):

#     return render(request, "career_path_app/career_test.html")


class PredictView(APIView):
    def post(self, request):
        conn = http.client.HTTPSConnection("127.0.0.1", 5000)
        payload = 'json=1'
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        conn.request("POST", "/predict", payload, headers)
        res = conn.getresponse()
        data = res.read()
        return Response(data.decode("utf-8"), status=status.HTTP_200_OK)