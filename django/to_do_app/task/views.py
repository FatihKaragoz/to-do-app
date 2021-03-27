from django.shortcuts import render
# Create your views here.

from .models import Task, User
from .serializers import  TaskSerializer

from rest_framework import viewsets
from rest_framework import status

from rest_framework_jwt.authentication      import JSONWebTokenAuthentication

from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response    import Response
from rest_framework.generics    import RetrieveAPIView,ListCreateAPIView, CreateAPIView, GenericAPIView
from rest_framework.views   import APIView

from .serializers import UserLoginSerializer,TaskSerializer,UserSerializer


from datetime import datetime 

class UserLoginView(RetrieveAPIView):

    permission_classes = (AllowAny,)
    serializer_class = UserLoginSerializer
    def post(self, request):
        print(request.data)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = {
            'success' : 'True',
            'status_code'   : status.HTTP_200_OK,
            # 'full_name'     : User.objects.get(email=request.POST.get('email')).get_full_name(),
            # 'branch'        : User.objects.get(email=request.POST.get('email')).company,
            'message': 'Kullanıcı girişi başarılı',
            'token' : serializer.data['token'],
            'full_name' : serializer.data['full_name'],
            }
        status_code = status.HTTP_200_OK
        print(response)
        return Response(response, status=status_code)

class TaskListView(RetrieveAPIView):
    authentication_class    = JSONWebTokenAuthentication
    permission_classes      = (IsAuthenticated,)
 
    def post(self,request):
        
        if 'process' in request.data:
            if request.data['process'] == 'change':
                processed_task = Task.objects.get(id=request.data['id'])
                print("DATA CHANGED")
                processed_task.status = request.data['status']
                processed_task.completed_at = datetime.now()
                processed_task.save()
                return Response(
                    {   
                        'id':processed_task.id,
                        'status':processed_task.status,
                        'description': processed_task.description,
                        'assigned_user_id':processed_task.assigned_user_id,
                        'created_by_id':processed_task.created_by_id,
                        'completed_at' : processed_task.completed_at.strftime('%d:%m:%Y %H:%M'),
                        'id':processed_task.id
                    },status=200)

            elif request.data['process'] == 'new':
                try:
                    processed_task = Task.objects.create(
                        description = request.data['description'],
                        status = request.data['status'],
                        assigned_user_id = request.data['assigned_user_id'],
                        created_by_id = request.user.id
                        )
                    print("NEW DATA")   

                except Exception as e:
                    print(e)
                    return Response(status=400)

            return Response({'id':processed_task.id},status=200)
        
        tasks = Task.objects.all()
        
        return Response(TaskSerializer(tasks,many=True).data, status=200)
       
    def get(self,request):
        print(request.POST)
        print(request)
        return Response('------', status=200)

class UserListView(RetrieveAPIView):
    authentication_class    = JSONWebTokenAuthentication
    permission_classes      = (IsAuthenticated,)

    def post(self,request):
        users = User.objects.all()
        return Response(UserSerializer(users,many=True).data, status=200)
       
    def get(self,request):
        return 200

class RegisterView(RetrieveAPIView):
    authentication_class    = JSONWebTokenAuthentication
    permission_classes      = (AllowAny,)

    def post(self,request):
        if request.data:
            user = User.objects.create(
                email = request.data['email'],
                first_name = request.data['first_name'],
                last_name = request.data['last_name']
                )
            user.set_password(request.data['password'])
        return Response(status=200)
       
    def get(self,request):
        return 200
    
    