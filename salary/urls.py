from salary import views
from django.urls import re_path

app_name = 'salary'

urlpatterns = [
    re_path('^$', views.CcfsView.as_view(),name='ccfs'),
    # re_path('^$', views.AssistRegView.as_view(), name='assistreg'),
]