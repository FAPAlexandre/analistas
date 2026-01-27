
from django.contrib import admin
from django.urls import path
from metas import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('dashboard/', views.dashboard_metas, name='dashboard'),
    path('cadastro/', views.cadastro, name="cadastro"),
]
