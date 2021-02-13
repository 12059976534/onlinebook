from django.urls import path
from . import views
from .admincontroler import views as admin
from .profilecontroler import views as profile
from django.contrib.auth.views import PasswordResetView,PasswordResetDoneView,PasswordResetConfirmView,PasswordResetCompleteView

urlpatterns = [
   # reset pass============
   path('password_reset/',PasswordResetView.as_view(template_name='app/resetpas.html'),name='password_reset'),
   path('password/reset/done',PasswordResetDoneView.as_view(template_name='app/done.html'),name='password_reset_done'),
   path('password_reset_confim/<uidb64>/<token>/',PasswordResetConfirmView.as_view(template_name='app/confirm.html'),name="password_reset_confirm"),
   path('password_reset/complet',PasswordResetCompleteView.as_view(template_name='app/complete.html'),name='password_reset_complete'),
   # ======================
   path('',views.index,name='index'),
   path('search/',views.search,name="search"),
   path('register/',views.register,name='register'),
   path('palidacount/',views.palidacount,name='palidacount'),
   path('login/',views.login,name='login'),
   path('adminku/',admin.adminku,name='adminku'),
   path('tableadmin/',admin.tableadmin,name='tableadmin'),
   path('tablebuku/',admin.tablebuku,name='tablebuku'),
   path('tableuser/',admin.tableuser,name='tableuser'),
   path('newadmin/',admin.newadmin,name='newadmin'),
   path('uploadbuku/',views.uploadbuku,name='uploadbuku'),
   path('profile/',profile.profile,name='profile'),
   path('mybook/',profile.mybook,name='mybook'),
   path('logout/',views.logout,name='logout'),
   path('updateuser:<int:id>/',admin.updateuser,name='updateuser'),
   path('deletuser:<int:id>/',admin.deletuser,name='deletuser'),
   path('updatebuku<int:id>/',views.updatebuku,name='updatebuku'),
   path('deletbuku<int:id>/',views.deletbuku,name='deletbuku'),
   path('upaccount<int:id>/',profile.upaccount,name='upaccount'),
   path('some_view/',views.some_view,name='some_view'),
   path('baca<int:id>/',views.baca,name='baca'),
   path('bacabuku<int:id>/',views.bacabuku,name='bacabuku'),
   path('fetch/',views.post_fect,name='fetch'),
   path('postsearch/',views.post_search,name='postsearch'),
   
]
