from django.conf.urls import url

from App import views, mine

urlpatterns = [
    url(r'^$', views.index, name='index'),

    url(r'^product/(?P<sid>\d+)/$', views.product, name='product'),
    url(r'^product/(?P<sid>\d+)/(?P<tag>\d+)/$', views.product, name='product'),

    url(r'^account/$', views.account, name='account'),
    url(r'^register/$', views.register, name='register'),
    url(r'^user_logout/$', views.user_logout, name='user_logout'),

    url(r'^single/(?P<cid>\d+)/$', views.single, name='single'),

    url(r'^cart/$', views.cart, name='cart'),
    url(r'^additem/(?P<cid>\d+)/$', views.add_to_cart, name='additem'),
    url(r'^removeitem/(?P<cid>\d+)/$', views.remove_from_cart, name='removeitem'),
    url(r'^emptyitems/$', views.empty_from_cart, name='emptyitems'),

    url(r'^sellteaccounts/$', views.sellteaccounts, name='sellteaccounts'),
    url(r'^pay/$', views.pay, name='pay'),
    url(r'^finish/$', views.finish, name='finish'),
    url(r'^repay/$', views.repay, name='repay'),

    url(r'^orders/$', views.orders, name='orders'),
    url(r'^deleteorder/$', views.deleteorder, name='deleteorder'),

    url(r'^contact/$', views.contact, name='contact'),

    url(r'^confirm/$', views.confirm, name='confirm'),

    url(r'^password/$', views.newpassword, name='password'),
    url(r'^info/$', views.info, name='info'),
    url(r'^reset/$', views.reset, name='reset'),
    url(r'^reset_password/$',views.reset_password,name='reset_password'),

    url(r'^search/$', views.search, name='search'),

    url(r'^user/(?P<pk>\d+)/$', mine.UserAPIView.as_view(), name='user'),

]
