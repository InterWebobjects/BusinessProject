from django.conf.urls import url

from App import views, mine

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^product/(?P<sid>\d+)/$', views.product, name='product'),
    url(r'^product/(?P<sid>\d+)/(?P<tag>\d+)/$', views.product, name='product'),
    url(r'^account/$', views.account, name='account'),
    url(r'^register/$', views.register, name='register'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^single/$', views.single, name='single'),

    url(r'^cart/$', views.cart, name='cart'),

    url(r'^user/(?P<pk>\d+)/$', mine.UserAPIView.as_view(), name='user'),

]
