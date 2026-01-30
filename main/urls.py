"""from django.urls import path
from . import views

urlpatterns = [
    path('export/', views.export_iris_csv, name='export_csv'),
    path('import/', views.import_iris_csv, name='import_csv'),
]
"""
"""
from django.urls import path, include
from django.contrib.auth import views as auth_views
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'api/iris', views.IrisPlantViewSet)

urlpatterns = [
    path('', views.search_view, name='home'),
    path('export/', views.export_iris_csv, name='export_csv'),
    path('import/', views.import_iris_csv, name='import_csv'),
    path('list/', views.list_view, name='list_view'),
    path('add/', views.add_view, name='add_view'),
    path('delete/<int:id>/', views.delete_view, name='delete_view'),
    path('search/', views.search_view, name='search_view'),
    path('predict/', views.predict_view, name='predict_view'),
    path('register/', views.register_view, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('', include(router.urls)),
]
"""

from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

# API Yönlendiricisi (Router)
router = DefaultRouter()
router.register(r'api/plants', views.IrisPlantViewSet)

urlpatterns = [
    # Sayfa Yönlendirmeleri
    path('', views.list_view, name='list_view'),
    path('list.html', views.list_view, name='list_html'),
    path('add.html', views.add_view, name='add_view'),
    path('search.html', views.search_view, name='search_view'),
    path('predict.html', views.predict_view, name='predict_view'),
    path('register.html', views.register_view, name='register_view'),
    
    # İşlevsel Yönlendirmeler (Silme, CSV)
    path('delete/<int:id>/', views.delete_view, name='delete_view'),
    path('export/', views.export_iris_csv, name='export_iris_csv'),
    path('import/', views.import_iris_csv, name='import_iris_csv'),

    # API URL'leri
    path('', include(router.urls)),
]