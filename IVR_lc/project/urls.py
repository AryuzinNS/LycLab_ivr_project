"""
URL configuration for project project.

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
from main import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('registration/', views.registration_page, name="Регистрация"),
    path('', views.index_page, name="Главная"),
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout, name="Выйти"),
    path('profile/<int:id>/', views.profile_page, name="Чей-то профиль"),
    path('profile/', views.profile_page, name="Профиль"),
    path('workbench/', views.verstak, name="Рабочая платформа"),
    path('rickroll/', views.rick, name="Rickroll"),
    path('all_theory/',views.all_theory,name="Все теоретические материалы"),
    path('all_theory/theory/<int:id>/',views.theory, name="Лабораторная работа"),
    path('create/',views.create_theory,name="Создать теоретическую справку"),
    path('profile/edit/',views.profile_editor, name= "Редактировать профиль"),
    path('theory_change/<int:id>/',views.edit_theory, name= "Изменить лабораторную работу"),
    path('sim/',views.sim, name="1111111"),
]
