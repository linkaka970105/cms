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
from django.contrib import admin

from goods import views

urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    # url(r'^test/$', views.test),
    url(r'^goods/categories/$', views.GoodsCategoryView.as_view()),
    url(r'^goods/categories2/$', views.GoodsCategoryView2.as_view()),
    url(r'^goods/slides/$', views.GoodsSlideView.as_view()),
    url(r'^goods/recommend/$', views.GoodsRecommendView.as_view()),
    url(r'^goods/$', views.GoodsListView.as_view({'get':'list'})),
    url(r'^goods/(?P<pk>\d+)/$', views.GoodsListView.as_view({'get': 'retrieve'})),
    url(r'^goods/bread/(?P<pk>\d+)/$', views.GoodsBreadView.as_view()),
]
