from django.conf.urls import url
from . import views

app_name = 'coursenotes'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<course_slug>[\w-]+)/$', views.course_index, name='course_index'),
    url(r'^(?P<course_slug>[\w-]+)/ch/(?P<ch_num>[0-9]+)/$', views.chapter_view, name='chapter_view'),
    url(r'^(?P<course_slug>[\w-]+)/info/$', views.course_info_page, name='course_info')
]
