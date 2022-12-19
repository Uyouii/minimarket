from django.conf.urls import patterns, url

import comment

urlpatterns = patterns(
    '',
    url(r'^id/(?P<comment_id>\d+)/$',
        comment.getCommentByIdApi,
        name='getCommentByIdApi'),
    url(r'^addcomment/', comment.addCommentToProductApi, name='addCommentToProductApi'),
    url(r'^responsecomment/', comment.addResponseToCommentApi, name='addResponseToCommentApi'),
    url(r'^productcomments/', comment.getProductCommentApi, name='getProductCommentApi'),
    url(r'^commentresponses/', comment.getCommentResponseApi, name='getCommentResponseApi'),
)
  