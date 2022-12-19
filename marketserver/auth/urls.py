from django.conf.urls import patterns, url

import auth

urlpatterns = patterns(
    '',
    url(r'^register/', auth.userRegister, name='register'),
    url(r'^login/', auth.userLogin, name='login'),
)
