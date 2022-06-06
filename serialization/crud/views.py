from urllib import response
from django.shortcuts import render
import io
# from elastic_transport import Serializer
from numpy import fromregex
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from django.http import HttpResponse
from .models import Student
from .serializers import StudentSerializer, StudSerializer
from django.views.decorators.csrf import csrf_exempt

from rest_framework.decorators import api_view
from rest_framework.response import Response

# from django.shortcuts import render
# from rest_framework.response import Response
# from .models import Student
from rest_framework import status
from rest_framework import viewsets

from rest_framework.generics import ListAPIView
from .mypaginations import MyPageNumberPagination, MyLimitOffsetPagination


@csrf_exempt
def student_api(request):
    #for retriving
    if request.method == 'GET':
        json_data = request.body
        stream = io.BytesIO(json_data)
        pythondata = JSONParser().parse(stream) #CONVERTED RETRIVING REQUEST JSON DATA INTO PYTHON DATA 
        id = pythondata.get('id', None) # to get id for retriving info perpose

        if id is not None:
            stu = Student.objects.get(id=id)
            serializer = StudentSerializer(stu)
            json_data = JSONRenderer().render(serializer.data) #to give response to api client
            return HttpResponse(json_data, content_type='application/json')

        #if id is none then have to retrive all data
        stu = Student.objects.all()
        serializer = StudentSerializer(stu, many=True)
        json_data = JSONRenderer().render(serializer.data) #to give response to api client
        return HttpResponse(json_data, content_type='application/json')

    #for creating new data
    if request.method == 'POST':
        #WE HAVE TO CONVERT JSON DATA WHICH IS COMMING FROM CLIENTSIDE(MYAPP.PY post request) into python data
        # along with have to send one response to client too
        json_data = request.body
        stream = io.BytesIO(json_data)
        pythondata = JSONParser().parse(stream) 
        serializer = StudentSerializer(data = pythondata) #conversion of python data into complex data and save it to table
        if serializer.is_valid():
            serializer.save()
            res = {'msg': 'new data created'}
            json_data = JSONRenderer().render(res) 
            return HttpResponse(json_data, content_type='application/json')
        json_data = JSONRenderer().render(serializer.errors) 
        return HttpResponse(json_data, content_type='application/json')

    if request.method == 'PUT':
        json_data = request.body
        stream = io.BytesIO(json_data)
        pythondata = JSONParser().parse(stream)
        id = pythondata.get('id')
        stu = Student.objects.get(id=id)
        serializer = StudentSerializer(stu, data=pythondata, partial=True)
        if serializer.is_valid():
            serializer.save()
            res = {'msg': 'data updated!!'} 
            json_data = JSONRenderer().render(res) 
            return HttpResponse(json_data, content_type='application/json')
        json_data = JSONRenderer().render(serializer.errors) 
        return HttpResponse(json_data, content_type='application/json')

    if request.method == 'DELETE':
        json_data=request.body
        stream=io.BytesIO(json_data)
        pythondata=JSONParser().parse(stream)
        id=pythondata.get('id')
        stu=Student.objects.get(id=id)
        stu.delete()
        res = {'msg': 'data deleted'}
        json_data = JSONRenderer().render(res) 
        return HttpResponse(json_data, content_type='application/json')



# FUNCTION BASED API VIEW
# this is better and short option of code above

# @api_view()
# def hello_world(request):
#     return Response({'msg': 'This is GET request'})

@api_view(['POST', 'GET'])
def hello_world(request):
    if request.method == 'GET':
        return Response({'msg': 'This is GET response'})

    if request.method == 'POST':
        print(request.data)  # request.data hase our current parsed data
        return Response({'msg': 'This is POST response', 'data':request.data})


# viewset 
# this is better and short option of code above
class StudentViewSet(viewsets.ViewSet):
    def list(self, request):
        stu = Student.objects.all()
        Serializer = StudentSerializer(stu, many=True)
        return Response(Serializer.data)

    def retrieve(self, request, pk=None):
        id = pk
        if id is not None:
            stu = Student.objects.get(id=id)
        Serializer = StudentSerializer(stu )
        return Response(Serializer.data)

    def create(self, request):
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg' : 'data is created'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, pk):
        id = pk
        stu = Student.objects.get(id=id)
        serializer = StudentSerializer(stu, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg' : 'data is created'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk):
        id = pk
        stu = Student.objects.get(pk=id)
        serializer = StudentSerializer(stu, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()     
            return Response({'msg': 'Partial data updated'})
        return Response(serializer.errors)

    def destroy(self, request, pk):
        print("DESTROID")
        print("basename : ", self.basename)
        print("action : ", self.action)
        print("detail : ", self.detail)
        print("suffix : ", self.suffix)
        print("name : ", self.name)
        print("description  : ", self.description)
        id = pk
        stu = Student.objects.get(pk=id)
        stu.delete()
        return Response({'msg': 'data deleted'})


#  pagination, offset

class StudentList(ListAPIView):
    queryset = Student.objects.all()
    serializer_class = StudSerializer
    # pagination_class = MyPageNumberPagination
    pagination_class = MyLimitOffsetPagination

# if we want defalult pagination provided by REST then we have to write only here,
# no need to create new subclass , which is at mypaginations.py




