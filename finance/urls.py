from django.conf.urls import url
from . import views

app_name = 'finance'

urlpatterns = [
    url(r'^$', views.basic_view, name='basic_view'),
    url(r'^edit/([0-9]+)/$', views.populated_basic_view, name='populated_basic_view'),
    url(r'^submitchangestable/$', views.sumbit_changes_in_table, name='sumbit_changes_table'),
    url(r'^submittransactionform/$', views.submit_transaction_form, name='submit_transaction_form')
]
