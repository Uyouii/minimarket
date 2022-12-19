from django.conf.urls import patterns, include, url

urlpatterns = patterns(
    '',
    url(r'^auth/', include('auth.urls')),
    url(r'^product/', include('product.urls')),
    url(r'^comment/', include('comment.urls')),
)
