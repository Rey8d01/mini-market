"""api_market URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
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
from .views import ItemViewSet, OrdersViewSet, CartViewSet, AuthView, CartDetail, UserDetail

urlpatterns = [
    # /home
    # url(r'^catalogs/$', ItemList.as_view()),
    # /items
    # url(r'^catalog-list/$', ItemViewSet.as_view({'get': 'list'})),
    url(r'^catalog-item/(?P<catalogAlias>[\w-]+)$', ItemViewSet.as_view({'get': 'list'})),

    # url(r'^orders$', OrdersViewSet.as_view({'get': 'list'})),

    url(r'^auth', AuthView.as_view()),
    url(r'^profile$', UserDetail.as_view()),
    url(r'^cart$', CartDetail.as_view()),


    # /catalog/:catalogAlias/:page?tags

]
