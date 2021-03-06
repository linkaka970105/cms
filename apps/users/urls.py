"""cms URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from rest_framework_jwt.views import obtain_jwt_token

from users import views

urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url(r'^test/$', views.test),
    url(r'^user/count/(?P<pk>\w{5,20})$', views.CheckUsername.as_view()),
    url(r'^user/regiuser/$', views.RegiUser.as_view()),
    url(r'^user/area/$', views.AreaP.as_view()),
    url(r'^user/area/(?P<pk>\d+)/$', views.AreaC.as_view()),
    url(r'^user/addlicr/$', views.Create_Area.as_view()),
    url(r'^user/updad/(?P<pk>\d+)/$', views.Update_Defadd.as_view()),
    url(r'^user/delad/(?P<pk>\d+)/$', views.DelAddr.as_view()),

    url(r'^authorizations/$', obtain_jwt_token),
]
