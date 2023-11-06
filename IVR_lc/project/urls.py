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
    #Администрирование
    path('admin/', admin.site.urls),
    #Регистрация пользователя
    path('registration/', views.registration_page, name="Регистрация"),
    #Главная страница
    path('', views.index_page, name="Главная"),
    # Страница авторизации
    path('login/', views.login_page, name='login'),
    # Функция выхода из профиля
    path('logout/', views.logout, name="Выйти"),
    # Страница просмотра профиля
    path('profile/<int:id>/', views.profile_page, name="Чей-то профиль"),
    # Страница профиля после регистрации
    path('profile/', views.profile_page, name="Профиль"),
    # Страница среды выполения работы
    path('workbench/', views.verstak, name="Рабочая платформа"),
    # Доступ ко всем  теоретическим материалам
    path('all_theory/',views.all_theory,name="Все теоретические материалы"),
    # Доступ к конкретной лабораторной работе
    path('all_theory/theory/<int:id>/',views.theory, name="Лабораторная работа"),
    # Страница добавления теории для пользователей категории учитель
    path('create/',views.create_theory,name="Создать теоретическую справку"),
    # Страница редактирования профиля
    path('profile/edit/',views.profile_editor, name= "Редактировать профиль"),
    # Страница изменения теоретических материалов для пользователей категории учитель
    path('theory_change/<int:id>/',views.edit_theory, name= "Изменить лабораторную работу"),
    # Сброс поискового запроса
    path('all_theory/reset/', views.reset_filter, name="сброс фильтра"),
    # Страница ввода и проверки адреса элеткронной почты для восстановления пароля
    path('email_enter/', views.EnterEmail),
    # Страница восстановления пароля, если пользователь его забыл
    path('password_reset/', views.ResetPasswd),

]
