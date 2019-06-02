# by EMILIO
# Contains all the URL paths of the website
# this determines website addresses, how its named, and what view it connects to


from django.urls import path
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from . import views

from .models import Post


from django.views.generic.base import RedirectView

urlpatterns = [
    path('', views.index2, name = 'index'),

    path('about', views.aboutIndex, name = 'about'),
    path('AboutAndrew', views.aboutAndrew, name='aboutAndrew'),
    path('AboutPreston', views.aboutPreston, name='aboutPreston'),
    path('AboutSahas', views.aboutSahas, name='aboutSahas'),
    path('AboutConnor', views.aboutConnor, name='aboutConnor'),
    path('AboutEmilio', views.aboutEmilio, name='aboutEmilio'),
    path('AboutMarcelo', views.aboutMarcelo, name='aboutMarcelo'),
    path('AboutPeitong', views.aboutPeitong, name='aboutPeitong'),

    path('index2', views.index2, name='index2'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='login'),
    path('register', views.register, name='register'),
    path('register2', views.register2, name='register2'),
    path('forgotpassword', views.forgotpassword, name='forgotpassword'),
    path('submit', views.HazardUpload, name='Upload'),
    path('submit2', views.HazardUpload2, name='Upload2'),
    path('searchresults2', views.searchresults2, name='searchresults2'),
    #path('post', views.hazardPost, name='post'),

    #Detailed hazard page
    url(r'^post/(?P<id>\d+)/$', views.hazardPost, name='post'),

    #Admin Index
    path('admin', views.admin, name='admin'),
    #Admin deleting a post LISTING
    path('adminDelete', views.adminDelete, name='adminDelete'),
    #Admin banning a user LISTING
    path('adminBan', views.adminBan, name='adminBan'),

    #Admin approving and rejecting posts
    url(r'^approve/(?P<id>\d+)/$', views.hazardApprove, name='approve'),
    url(r'^reject/(?P<id>\d+)/$', views.hazardReject, name='reject'),
    #Admin deleting a post
    url(r'^delete/(?P<id>\d+)/$', views.hazardDelete, name='delete'),
    #Admin banning a user
    url(r'^pban/(?P<uname>[\w.@+-]+)/$', views.userPBan, name='pban'),
    url(r'^tban/(?P<uname>[\w.@+-]+)/$', views.userTBan, name='tban'),
    #Admin unbanning a user
    url(r'^unban/(?P<uname>[\w.@+-]+)/$', views.userUnban, name='tban'),

    #Agent Index
    path('agent', views.agent, name='agent'),
    #Agent changing posts status
    url(r'^inprogress/(?P<id>\d+)/$', views.hazardInProgress, name='inprogress'),
    url(r'^finished/(?P<id>\d+)/$', views.hazardFinished, name='finished'),







    #Tab Icon
    url(r'^favicon.ico$', RedirectView.as_view(url='static/favicon.ico')),


]
