from django.conf.urls import url
from . import views

app_name = 'coursenotes'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^course/(?P<course_id>[0-9]+)/$', views.course_index, name='course_index'),
    url(r'^course/(?P<course_id>[0-9]+)/ch/(?P<ch_id>[0-9]+)/$', views.chapter_view, name='chapter_view'),
    url(r'^course/(?P<course_id>[0-9]+)/info/$', views.course_info_page, name='course_info')
]
