"""
URL configuration for BarDaPracaDarmas project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from bar import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('registro/', views.registro, name='registro'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('adicionar_produto/', views.adicionar_produto, name='adicionar_produto'),
    path('excluir_produto/<int:produto_id>/', views.excluir_produto, name='excluir_produto'),
    path('editar_produto/<int:produto_id>/', views.editar_produto, name='editar_produto'),
    path('reposicao_produto/<int:produto_id>/', views.reposicao_produto, name='reposicao_produto'),
    path('comprar/', views.comprar, name='comprar'),
    path('historico/', views.historico, name='historico'),
    path('historico_consumo/', views.historico_consumo, name='historico_consumo'),
    path('deletar_historico/', views.deletar_historico, name='deletar_historico')
]
