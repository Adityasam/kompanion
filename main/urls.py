from . import views
from django.urls import path

app_name="main"

urlpatterns=[
    path('', views.original_home, name="original_home"),
    path('home/',views.home,name='home'),
    path('logout/',views.logouts,name="logout"),
    path('admin_page/',views.admin_page,name="admin_page"),
    path('detail/<center_id>',views.detail,name="detail"),
    path('allot_center/', views.allot_center, name="allot_center"),
    path('center_detail/<center_id>',views.center_detail, name="center_detail"),
    path('tablet_transfer/<tid>/<center_id>', views.tablet_transfer, name="tablet_transfer"),
    path('transfer/',views.transfer, name="transfer"),
    path('login/',views.login, name="login"),
    path('centers/', views.centers, name="centers"),
    path('tobe/',views.tobe, name="tobe"),
    path('mark_received/<tid>/', views.mark_received, name="mark_received"),
    path('allot_from_center/', views.allot_from_center, name="allot_from_center"),
    path('mark_damaged/<tid>/',views.mark_damaged, name="mark_damaged"),
    path('mark_completed/<tid>/',views.mark_complete, name="mark_complete"),
    path('update_tablet/<tid>/', views.update_tablet, name="update_tablet"),
    path('delete_tab/<tid>/<cid>/', views.delete_tab, name="delete_tab"),
    path('tablet_history/<tid>/', views.tablet_history, name="tablet_history"),
]