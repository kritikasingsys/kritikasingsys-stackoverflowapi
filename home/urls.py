from django.conf.urls import url, include

from . import views
urlpatterns = [
    url(r'^$',views.BasicHtmlView.as_view(),name='base'),
    url(r'stack_search/$',views.StackOverflowForm.as_view(),name='stack_search')
]