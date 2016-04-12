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
from .views import ProductsViewSet, OrderViewSet, AuthView, CartDetail, UserDetail, CatalogListViewSet, CatalogItemViewSet, TagsViewSet

urlpatterns = [
    url(r'^catalog-list$', CatalogListViewSet.as_view({'get': 'list'})),
    url(r'^catalog-item/(?P<alias>[\w-]+)$', CatalogItemViewSet.as_view({'get': 'retrieve'})),
    url(r'^tags$', TagsViewSet.as_view({'get': 'list'})),
    url(r'^products/(?P<alias>[\w-]+)$', ProductsViewSet.as_view({'get': 'list'})),

    url(r'^auth', AuthView.as_view()),
    url(r'^profile$', UserDetail.as_view()),
    url(r'^cart$', CartDetail.as_view()),
    url(r'^order$', OrderViewSet.as_view({'get': 'list'})),
    url(r'^order/(?P<order_id>[\d]+)$', OrderViewSet.as_view({'get': 'retrieve'})),
]
