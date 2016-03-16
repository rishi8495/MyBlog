from django.conf import settings
from django.conf.urls import include, url

from .views import BlogDetailView, BlogListView, CreateBlogView, DraftView, TagView

urlpatterns = [
	url(r'^$',BlogListView.as_view(),name='blogs'),
	url(r'^blog/(?P<slug>[-\w]+)/$',BlogDetailView.as_view(),name='blog'),
	url(r'^drafts/$', DraftView.as_view(), name='drafts'),
	url(r'^blog-new/$', CreateBlogView.as_view(), name='new'),
	url(r'^post/tag/(?P<tag_name>.+)$', TagView.as_view(), name='tag'),

]

