from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.generics import (CreateAPIView, ListCreateAPIView,
                                     RetrieveUpdateDestroyAPIView)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Users
from .serializers import UserLoginSerializer, UsersSerializers


# Vista o endpoint para crear un usuario y listar todos los ya registrados.
class UsersPostGet(ListCreateAPIView):
    queryset = Users.objects.all()
    serializer_class = UsersSerializers
    
    # Se crea un usuario de django, se genera un token y se le asigna antes de guardar los datos.
    def create(self, request, *args, **kwargs):
        serializer = UsersSerializers(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data

            username = '_'.join([validated_data.get('first_name'),validated_data.get('last_name')])
            password = validated_data.get('password')
            email = validated_data.get('email')
            created_django_user = User.objects.create_user(username, email, password)

            user_token = Token.objects.create(user=created_django_user)
            
            serializer.save(username = created_django_user, token= user_token.key)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Vista o endpoint para obtener, actualizar y eliminar un usuario por su id
class UserGetPutDelete(RetrieveUpdateDestroyAPIView):
    serializer_class = UsersSerializers
    queryset = Users.objects.all()
    lookup_field = 'pk'
    permission_classes = [IsAuthenticated]
    
    # Se elimina el usuario-django enlazado al username del Usuario
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        django_user_to_delete = User.objects.get(username=instance.username)
        self.perform_destroy(instance)
        django_user_to_delete.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



# Vista o endpoint para el login de usuarios
class UsersLogin(CreateAPIView):
    serializer_class = UserLoginSerializer

    # Se obtiene el username y password, se verifica que el usuario existe y se retorna su token
    def create(self, request, *args, **kwargs):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            users_object = get_object_or_404(Users, mobile_phone=validated_data.get('mobile_phone'))
            username = users_object.username
            password = validated_data.get('password')

            user_is_registered = authenticate(username=username, password=password)
            if user_is_registered:
                token_user ={'Token': users_object.token}
                return Response(token_user, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)
