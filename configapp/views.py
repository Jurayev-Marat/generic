from django.shortcuts import render, get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from .serializers import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import *
from rest_framework.views import *
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated


# Create your views here.

class OrderModelViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializers


class CustomerModelViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializers


class EmployeesModelViewSet(ModelViewSet):
    queryset = Employees.objects.all()
    serializer_class = EmployeesSerializers


class MovieModelViewSet(ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializers

    @action(detail=True, methods=['post'])
    def add_actor(self, request, *args, **kwargs):
        actor_id = request.data['actor_id']
        movie = self.get_object()
        movie.actor.add(actor_id)
        movie.save()
        serializer = ModelSerializer(movie)
        return Response(data=serializer.data)

    @action(detail=True, methods=['delete'])
    def remove_actor(self, request, *args, **kwargs):
        actor_id = request.data.get('actor_id')
        movie = self.get_object()
        movie.actor.remove(actor_id)
        movie.save()
        serializer = ModelSerializer(movie)
        return Response(data=serializer.data)


class ActorModelViewSet(ModelViewSet):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializers

    @action(detail=True, methods=['get'])
    def get(self, request, *args, **kwargs):
        actors = self.get_queryset()
        serializer = self.serializer_class(actors, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['delete'])
    def delete(self, request, *args, **kwargs):
        actor = self.get_object()
        actor.delete()
        return Response({"massage": "Actor delete successfully"}, status=status.HTTP_204_NO_CONTENT)


class CommitApi(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        response = {'success': True}
        commits = CommitMovie.objects.filter(author=request.user)
        serializer = CommitSerializers(commits, many=True)
        response['data'] = serializer.data
        return Response(response)

    @swagger_auto_schema(request_body=CommitSerializers)
    def post(self, request):
        response = {'success': True}
        serializer = CommitSerializers(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save(author=request.user)
            response['data'] = serializer.data
            return Response(response, status=201)
        return Response(serializer.errors, status=400)
