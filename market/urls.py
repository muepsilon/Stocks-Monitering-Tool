"""market URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token
import stocks.views as views
import mutualfund.views as mfviews
import login.views as login_views
from stocks.models import Stock, WatchStock
from django.http import HttpResponseRedirect
from rest_framework import routers, serializers, viewsets

# Serializers define the API representation.
class StockSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Stock
        fields = ('company_name', 'symbol', 'invested_price', 'N_stocks','target_price','trigger_price_high','trigger_price_low')

# ViewSets define the view behavior.
class StockViewSet(viewsets.ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer

class WatchStockSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = WatchStock
        fields = ('company_name', 'symbol', 'trigger_price_high','trigger_price_low')

# ViewSets define the view behavior.
class WatchStockViewSet(viewsets.ModelViewSet):
    queryset = WatchStock.objects.all()
    serializer_class = WatchStockSerializer

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'stocks', StockViewSet)
router.register(r'watchstocks', WatchStockViewSet)

urlpatterns = [
    url(r'^api/accounts/login/$', login_views.loginUser, name="login_user"),
    url(r'^api/accounts/logout/$', login_views.logoutUser, name="logout_user"),
    url(r'^api/accounts/signup/$', login_views.signupUser, name="signup_user"),
    url(r'^api/accounts/verifysession/$', login_views.is_logged_in, name="logged_in_status"),
    url(r'^api/company/find/$',views.getCompanyNames, name="get_company_names"),
    url(r'^api/company/(?P<symbol>[a-zA-Z]+)$',views.company_info, name="comapany_info"),
    url(r'^api/latestprice/stocks/$',views.portfolio, name="portfolio"),
    url(r'^api/latestprice/watchstocks/$',views.watchlist, name="watchList"),
    url(r'^api/latestprice/indices/$',views.get_index_info, name="index quotes"),
    url(r'^api/', include(router.urls,namespace="api")),
    url(r'^api-token-refresh/', refresh_jwt_token),
    url(r'^api-token-verify/', verify_jwt_token),
    url(r'^api-token-auth/', obtain_jwt_token),
    url(r'^$', views.index, name="index"),
    url(r'^test/$',views.example_view),
    url(r'^updatedb/$', mfviews.update_database),
    url(r'^company/(?P<page_slug>[\w-]+)$', views.index, name="angular_router"),
    url(r'^accounts/*',views.index, name = "angular_router"),
]
