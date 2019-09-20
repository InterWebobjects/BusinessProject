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

    url(r'^user/(?P<pk>\d+)/$', mine.UserAPIView.as_view(), name='user'),
    url(r'^cart/(?P<pk>\d+)/$', mine.CartAPIView.as_view(), name='user'),

]
