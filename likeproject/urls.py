from django.contrib import admin
from django.urls import path
from like import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name="home"),
    path('<int:post_id>/', views.detail, name="detail"),
    path('new/', views.new, name="new"),
    path('<int:post_id>/edit', views.edit, name="edit"),
    path('<int:post_id>/delete', views.delete, name="delete"),
    path('<int:post_id>/comment/create/', views.comment_create, name="comment_create"),
    path('<int:post_id>/comment/<int:comment_id>/delete', views.comment_delete, name="comment_delete"),
    path('<int:post_id>/comment/<int:comment_id>/edit', views.comment_edit, name="comment_edit"),
    path('signup/', views.signup, name="signup"),
    path('signin/', views.signin, name="signin"),
    path('signout/',views.signout, name="signout"),
    path('<int:post_id>/post_like', views.post_like, name="post_like"),
]