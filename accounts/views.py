from datetime import datetime, timedelta
import pytz

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.core.mail import send_mail, BadHeaderError
from django.core.paginator import Paginator, EmptyPage
from django.views.generic import ListView
from django.db.models import Q

from .serializers import *
# from django.contrib.auth.models import User
from django.conf import settings

from .models import User
from opencivicdata.legislative.models import Event
from opencivicdata.core.models import Jurisdiction

from dex.serializers import EventSerializer

from rest_framework.settings import api_settings
from rest_framework import generics

from rest_framework.decorators import authentication_classes, permission_classes, api_view
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework import status
from rest_framework.response import Response

from rest_framework_jwt.authentication import JSONWebTokenAuthentication

tz_format = '%Y-%m-%dT$H:%M:%S+%H:%M'
td = timedelta(hours=18)
odt = datetime.now() - td
ndt = odt.strftime(tz_format)

###########
## Users ##
###########
@api_view(['POST'])
@permission_classes([])
def create_user(request):
    serialized = UserSerializer(data=request.data)
    print(request.data)
    if serialized.is_valid():
        serialized.save()
        return Response(serialized.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serialized._errors, status=status.HTTP_400_BAD_REQUEST)


@permission_classes([])
@authentication_classes([])
class UserProfileAPIView(generics.ListAPIView):
    serializer_class = UserProfileSerializer

    def get_queryset(self):
        print(self.request.path)
        path = self.request.path.split('/')[-2]
        queryset = User.objects.filter(username=path)
        return queryset


@permission_classes([])
@authentication_classes([])
class OpenJurisAPIView(generics.ListAPIView):
    serializer_class = MiniJurisSerializer

    def get_queryset(self):
        print(self.request.path)
        path = self.request.path.split('/')[-2]
        jurisdictions = Jurisdiction.objects.all()
        ujuris = UserJurisdictions.objects.filter(activist__username=path)
        juris = []
        for j in ujuris:
            juris.append(j.jurisdiction)
        queryset = list(set(jurisdictions).difference(set(juris)))
        print(queryset)
        return queryset


@permission_classes([])
@authentication_classes([])
class UsersAPIView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer



@permission_classes([])
@authentication_classes([])
class UserEventsAPIView(generics.ListAPIView):
    serializer_class = EventSerializer

    def get_queryset(self):
    	qs = []
    	path = self.request.path.split('/')[-2]
    	user = User.objects.filter(username=path)[0]
    	juris = user.userjurisdictions_set.all()
    	jids = []
    	for j in juris:
    		jids.append(j.jurisdiction.id)
    	print('jids', jids)
    	queryset = Event.objects.filter(jurisdiction__in=jids, start_date__gte=ndt)
    	print(queryset)
    	return queryset.order_by('start_date')


@permission_classes([])
@authentication_classes([])
class UserAPIView(generics.ListAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        print(self.request.path)
        path = self.request.path.split('/')[-2]
        queryset = User.objects.filter(username=path)
        return queryset


@api_view(['POST'])
@permission_classes([])
@authentication_classes((JSONWebTokenAuthentication,))
def add_user_deets(request):
    print(request.data)
    print(request.user)
    data = request.data
    user = User.objects.get(username=data['username'])
    user.email = data['email']
    user.phone_number = data['phone']
    user.save()
    try:
        print('user', user)
        serialized = UserProfileSerializer(user)
        print('serialized', serialized)
        return Response(serialized.data, status=status.HTTP_201_CREATED)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([])
@authentication_classes([])
def add_juris(request):
    print(request.data)
    if request.data['activist'][0].isalpha():
        user = User.objects.get(username=request.data['activist'])
        request.data['activist'] = user.id

    serialized = JurisSerializer(data=request.data)

    if serialized.is_valid():
        serialized.save()
        return Response(serialized.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serialized._errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([])
@authentication_classes([])
def add_organizer(request):
	serialized = OrganizerSerializer(data=request.data)
	if serialized.is_valid():
		serialized.save()
		return Response(serialized.data, status=status.HTTP_201_CREATED)
	else:
		return Response(serialized._errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([])
@authentication_classes([])
def add_orgs(request):
	data = request.data
	serialized = OrgFollowsSerializer(data=data)
	if serialized.is_valid():
		serialized.save()
		return Response(serialized.data, status=status.HTTP_201_CREATED)
	else:
		return Response(serialized._errors, status=status.HTTP_400_BAD_REQUEST)

