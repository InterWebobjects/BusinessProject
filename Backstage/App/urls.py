from django.conf.urls import url

from App import views

urlpatterns = [

    url(r'^$', views.index, name='index'),
    url(r'^index/$', views.index_Desktop, name='Desktop'),
    url(r'^welcome/$', views.welcome, name='welcome'),
    url(r'^welcome/(?P<page>\d+)$', views.welcome, name='welcome'),
    url(r'^users/$', views.users, name='users'),
    url(r'^student/$', views.students_Add, name='students'),
    url(r'^student/(?P<page>\d+)/$', views.students_Add, name='students'),

    url(r'^add_student/$',views.add_user,name='add_shudent'),
    url(r'^add_student/(?P<page>\d+)/$',views.add_user,name='add_shudent'),
    url(r'views/(?P<id>\d+)/',views.views_user,name='viewx'),
    url(r'^student_del/$', views.students_Del, name='students_del'),
    url(r'^student_del/(?P<page>\d+)$', views.students_Del, name='students_del'),
    url(r'^category/$', views.category, name='category'),
    # url(r'^category_add/$',views.category_add,name='category_add'),
    # url(r'^category_small/$',views.category_small,name='category_small'),
    url(r'^login/$', views.login, name='login'),
    url(r'^registered/$', views.registered, name='registered'),

    url(r'^commodity/(?P<page>\d+)/$', views.commodity_list, name='commodity'),
    url(r'^commodity/$', views.commodity_list, name='commodity'),
    url(r'^add_commodity/$', views.add_commodity, name='add_commodity'),
    url(r'^del_commodity/$', views.del_commodity, name='del_commodity'),
    url(r'^del_commodity/(?P<page>\d+)/$', views.del_commodity, name='del_commodity'),
    # 批量删除
    url(r'^batch_deletions/$', views.batchdeletion, name='batch_deletion'),
    url(r'^batch_deletions/(?P<page>\d+)/$', views.batchdeletion, name='batch_deletion'),
    url(r'^batch_restore/$', views.batchrestore, name='batch_restore'),
    url(r'^batch_restore/(?P<page>\d+)/$', views.batchrestore, name='batch_restore'),

]
