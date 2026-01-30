"""
URL configuration for iris_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path, include
from django.contrib.auth import views as auth_views
from rest_framework.routers import DefaultRouter

# DİKKAT: views.py 'main' klasöründe olduğu için 'main'den import ediyoruz
from main import views 

# API Router Tanımlaması
router = DefaultRouter()
router.register(r'api/plants', views.IrisPlantViewSet)

urlpatterns = [
    # --- Sayfa Yönlendirmeleri ---
    path('', views.list_view, name='list_view'),
    path('list.html', views.list_view, name='list_html'),
    path('add.html', views.add_view, name='add_view'),
    path('search.html', views.search_view, name='search_view'),
    path('predict.html', views.predict_view, name='predict_view'),
    path('register.html', views.register_view, name='register_view'),
    
    # --- Kullanıcı İşlemleri (Login/Logout/Register) ---
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', views.register_view, name='register_view'),

    # --- Şifre Sıfırlama (Ödev Gereksinimi) ---
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='password_reset.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),

    # --- İşlevsel Yönlendirmeler (CRUD & CSV) ---
    path('add/', views.add_view, name='add_view_func'), # Fonksiyonel path
    path('update/<int:id>/', views.update_view, name='update_view'), # Güncelleme
    path('delete/<int:id>/', views.delete_view, name='delete_view'), # Silme
    path('export/', views.export_iris_csv, name='export_iris_csv'), # CSV İndir
    path('import/', views.import_iris_csv, name='import_iris_csv'), # CSV Yükle
    path('predict/', views.predict_view, name='predict_view_func'), # Tahmin POST

    # --- API URL'leri ---
    path('', include(router.urls)),
]
