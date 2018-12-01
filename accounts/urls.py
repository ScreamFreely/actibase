from django.conf.urls import url
from django.views.generic import DetailView
from rest_framework.urlpatterns import format_suffix_patterns

from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token,verify_jwt_token

from .views import *

urlpatterns = [
    url(r'^auth/refreshtoken/', refresh_jwt_token),
    url(r'^auth/obtaintoken/', obtain_jwt_token),
    url(r'^api/users$', UsersAPIView.as_view(), name="users"),  
    url(r'^api/user/[-@\w]+/$', UserAPIView.as_view(), name="user"),  
    url(r'^updateuser/', add_user_deets, name="updateuser"),
    url(r'^api/profile/[-@\w]+/$', UserProfileAPIView.as_view(), name="profile"),  
    url(r'^api/userevents/[-@\w]+/$', UserEventsAPIView.as_view(), name="userevents"), 

    url(r'^createuser/', create_user, name="user"), 
    url(r'^createjuriuser/', add_juris, name="juri-user"),
    url(r'^createorganizer/', add_orgs, name="add-organizer"),
    url(r'^followorg/', add_orgs, name="add-orgs"),

    url(r'^orgdiff/[-@\w]+/$', OpenJurisAPIView.as_view(), name="diff-orgs"),
]
