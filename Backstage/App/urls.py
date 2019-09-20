from django.conf.urls import url

from App import views

urlpatterns = [

    url(r'^$', views.index, name='index'),
    url(r'^index/$', views.index_Desktop, name='Desktop'),
    url(r'^welcome/$', views.welcome, name='welcome'),
    url(r'^users/$', views.users, name='users'),
    url(r'^student/$', views.students_Add, name='students'),
    url(r'^student/(?P<page>\d+)/$', views.students_Add, name='students'),
    url(r'^student_del/$', views.students_Del, name='students_del'),
    url(r'^category/$', views.category, name='category'),
    # url(r'^category_add/$',views.category_add,name='category_add'),
    # url(r'^category_small/$',views.category_small,name='category_small'),
    url(r'^login/$', views.login, name='login'),
    url(r'^registered/$',views.registered,name='registered'),

    url(r'^commodity/(?P<page>\d+)/$',views.commodity_list,name='commodity'),
    url(r'^commodity/$',views.commodity_list,name='commodity'),
    url(r'^add_commodity/$',views.add_commodity,name='add_commodity'),

]
