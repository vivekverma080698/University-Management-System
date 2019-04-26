from authentication import views
from django.urls import re_path, include

app_name = 'authentication'

urlpatterns = [
    re_path('^$',views.IndexView.as_view(),name = 'Index',),
    re_path('^director/$', views.DirectorView.as_view(), name='director'),
    re_path('^registrar/$', views.RegistrarView.as_view(), name='registrar'),
    re_path('^assistreg/$', views.AssistRegView.as_view(), name='assistreg'),
    re_path('^hod/$', views.HodView.as_view(), name='hod'),
    re_path('^dfa/$', views.DfaView.as_view(), name='dfa'),
    re_path('^adfa/$', views.AdfaView.as_view(), name='adfa'),
    re_path('^deptsec/$', views.DeptSecView.as_view(), name='deptsec'),
    re_path('^ccfs/', include('salary.urls',namespace='salary'),name='ccfs'),
    re_path('^faculty/$', views.FacultyView.as_view(), name='faculty'),
    re_path('^staff/$', views.StaffView.as_view(), name='staff'),
    re_path('^logout/$', views.logout_view, name='logout')
]


