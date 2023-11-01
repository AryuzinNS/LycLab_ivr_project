from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from main.forms.forms import RegForm, LoginForm, AddTheoryForm, ProfEditForm, EditTheoryForm, SearchPrForm
from main.models import Profile, Theory
from django.http.request import HttpRequest
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.views.decorators.clickjacking import xframe_options_exempt
def index_page(request: HttpRequest ):
    """Обработчик страницы профиля"""
    context = {}
    context['author'] = 'Aryuzin Nikita'
    if auth.get_user(request).is_authenticated:
        id = get_user_id(request)
        prof = Profile.objects.get(id=id)
        context['id'] = id
        context['fullname'] = prof.fullname
    return render(request, 'index.html',context)

def get_user_id(request: HttpRequest):
    """
    Получение ID текущего пользователя

    :param request: Запрос пользователя
    :return: ID текущего пользователя
    """
    if auth.get_user(request).id:
        return int(auth.get_user(request).id)
def registration_page(request: HttpRequest):
    """
    Страница регистрации

    :param request: Запрос пользователя
    """
    context = {'pagename': 'Регистрация', 'error': ''}
    if request.method == "POST":
        form = RegForm(request.POST)
        if form.is_valid():
            if form.data["password"] == form.data["sec_password"]:
                user1 = User.objects.filter(username=form.data["username"])
                if not user1:
                    user = User(username=form.data["username"],
                                first_name=form.data["frst_name"],
                                last_name=form.data["last_name"])
                    user.set_password(form.data['password'])
                    user.save()
                    fullname = form.data["frst_name"]+" "+form.data["last_name"]
                    new_profile = Profile(fullname=fullname,
                                          age=21,
                                          isteacher=form.data["is_teacher"],
                                          user=user)
                    new_profile.save()

                    user = authenticate(username=form.data["username"], password=form.data["password"])
                    login(request, user)
                    url = '/profile/' + str(get_user_id(request))
                    return redirect("/")
                else:
                    context["error"] = "Этот юзернейм уже занят! Но Вы всегда можете выбрать другой"
        context["form"] = form
    else:
        context['form'] = RegForm(request.POST)
    return render(request, 'registration.html', context)


def login_page(request: HttpRequest):
    """
    Страница логина

    :param request: Запрос пользователя
    """
    context = {'user_id': get_user_id(request), "pagename": 'Авторизация'}
    if request.method == "GET":
        form = LoginForm()
        context['form'] = form
        if auth.get_user(request).is_authenticated:
            return redirect('/')

    if request.method == "POST":
        if auth.get_user(request).is_authenticated:
            return redirect('/')
        form = LoginForm(request.POST)
        if form.is_valid():
            context['form'] = form
            user = authenticate(username=form.data["username"], password=form.data["password"])
            if user:
                login(request, user)
                return redirect('/')

            redirect('/login')
            context["error"] = "Неправильный логин или пароль"
        else:
            return redirect('/login')

    return render(request, "login.html", context)

def logout(request: HttpRequest):
    """
    Выход из аккаунта

    :param request: Запрос пользователя
    :return: Перенаправление на главную страницу
    """
    auth.logout(request)
    return redirect('/')


@login_required(login_url="/login")
def profile_page(request: HttpRequest, id=-1):
    """
    Создаёт и возвращает страницу профиля пользователя.

    :param request: Запрос пользователя
    :return: Страница профиля пользователя
    """
    if id == -1:
        id = get_user_id(request)
    prof = Profile.objects.get(id=id)
    user = User.objects.get(id = id)
    context = {
        'name': prof.fullname,
        'login': user.username,
        'age': prof.age,
        'id': id,
        'pagename': "Профиль",
    }
    return render(request, "profile.html", context)

def rick(request: HttpRequest):
    """
    Создаёт и возвращает страницу рикролла ахахахах.

    :param request: Запрос пользователя
    :return: Физиономия проверяющего
    """
    context = {
       'pagename': "Never gonna give you up",
   }
    return render(request, "ricc.html", context)


@login_required(login_url="/login")
@xframe_options_exempt
def verstak(request: HttpRequest):
    """"
    Создает и возвращает страницу интерактивной доски
    :param request: Запрос пользователя
    :return: Страница интерактивной лаборатории
    """
    context = {
            "datetime": datetime.now(),
    }
    if request.user:
            context["user"] = request.user
    form = request.GET

    context['form'] = form
    return render(request, "workbench.html", context)
@xframe_options_exempt
def all_theory(request: HttpRequest):
    """Создает и возвращает страницу всех теоретических материалов
    :param request: Запрос пользователя
    :return: Страница с перечнем лабораторных работ
    """
    id = get_user_id(request)
    prof = Profile.objects.get(id=id)
    names = [work.name for work in Theory.objects.all()]
    works = []
    rq = ""
    if request.method == "POST":
        frm = SearchPrForm(request.POST)
        if frm.is_valid():
            if frm.data["text"]:
                rq = frm.data["text"]
                for i in range(len(names)):
                    if rq in names[i]:
                        works.append(Theory.objects.get(name=names[i]))
            else:
                works = Theory.objects.all()
    else:
        frm = SearchPrForm(request.POST)
        works = Theory.objects.all()
    context = {
        "datetime": datetime.now(),
        "pagename": "Теоретические материалы",
        "works": works,
        "isteacher": False,
        "form": frm,
    }
    if prof.isteacher==1:
        context["isteacher"] = True
    return render(request,"all_theory.html",context)

def reset_filter(request: HttpRequest):
    frm = SearchPrForm(request.POST)
    works = Theory.objects.all()
    context = {
        "datetime": datetime.now(),
        "pagename": "Теоретические материалы",
        "works": works,
        "isteacher": False,
        "form": frm,
    }
    redirect("/")
    return redirect("/all_theory/")


def theory(request: HttpRequest, id=-1):
    """
    Создает и возвращает страницу теоретических материалов по одной из лабораторных работ
    :param request: Запрос пользователя
    :return: Страница с теоретическими материалами лабораторной работы
    """
    id1 = get_user_id(request)
    prof = Profile.objects.get(id=id1)
    work = Theory.objects.get(id=id)
    context = {
        'id' : work.id,
        'title': work.name,
        'description': work.description,
        'file': work.file,
        "isteacher": False,
    }
    if prof.isteacher==1:
        context["isteacher"] = True
    context['pagename'] = 'Лабораторная работа | ' + context['title']
    return render(request, "labwrk.html", context)

def create_theory(request: HttpRequest):
    """
    Создает и возвращает страницу редактора теоретической справки для лабораторной работы
    :param request: Запрос пользователя
    :return: Страница редактора теоретических материалов
    """
    context = {'pagename': 'Редактор', 'error': ''}
    if request.method == "POST":
        form = AddTheoryForm(request.POST, request.FILES)
        if form.is_valid():
                new_theory = Theory(name=form.data["name"], description=form.data["description"], file=request.FILES["file"], user_id=auth.get_user(request).id)
                new_theory.save()
                url = '/all_theory/'
                return redirect(url)
        else:
                context["error"] = "Введенные данные не соответствуют формату"
        context["form"] = form
    else:
        context['form'] = AddTheoryForm(request.POST,request.FILES)
    return render(request, 'theory_editor.html', context)

@login_required(login_url="/login")
def profile_editor(request: HttpRequest ,id=-1):
    """
    Создает и возвращает страницу редактирования профиля пользователя
    :param request: Запрос пользователя
    :return: страница редактора профиля пользователя
    """
    id = get_user_id(request)
    prof = Profile.objects.get(id=id)
    user = User.objects.get(id= id)
    context = {'pagename': 'Редактировать профиль', 'error': ''}
    if request.method == "POST":
        form = ProfEditForm(request.POST)
        fullname = prof.fullname.split(' ')
        if len(fullname) == 2:
            form.fields["last_name"].widget.attrs["placeholder"] = f"Фамилия: {fullname[1]}"
        else:
            form.fields["last_name"].widget.attrs["placeholder"] = "Фамилия: "
        form.fields["username"].widget.attrs["placeholder"] = f"Логин: {user.username}"
        form.fields["first_name"].widget.attrs["placeholder"] = f"Имя: {prof.fullname[0]}"
        form.fields["age"].widget.attrs["placeholder"] = f"Возраст: {prof.age}"
        if form.is_valid():
            if form.data["password"] == form.data["sec_password"]:
                user.username = form.data["username"]
                user.set_password(form.data["password"])
                prof.fullname = form.data["first_name"]+" "+form.data["last_name"]
                user.first_name = form.data["first_name"]
                user.last_name = form.data["last_name"]
                prof.age = form.data["age"]
                prof.save()
                user.save()
                login(request, user)
                url = '/profile/' + str(prof.id)
                redirect("/")
                return redirect(url)
        else:
            context["error"] = "Введенные данные не соответствуют формату"
        context["form"] = form
    else:
        form = ProfEditForm(request.POST)
        fullname = prof.fullname.split(' ')
        form.fields["username"].widget.attrs["placeholder"] = f"Логин: {user.username}"
        form.fields["first_name"].widget.attrs["placeholder"] = f"Имя: {fullname[0]}"
        if len(fullname) == 2:
            form.fields["last_name"].widget.attrs["placeholder"] = f"Фамилия: {fullname[1]}"
        else:
            form.fields["last_name"].widget.attrs["placeholder"] = "Фамилия: "
        form.fields["age"].widget.attrs["placeholder"] = f"Возраст: {prof.age}"
        context['form'] = form
    return render(request, "profeditor.html", context)

def edit_theory(request: HttpRequest,id= -1):
    id1= int(request.get_full_path()[-2])
    theor = Theory.objects.get(id=id1)
    context = {'pagename': 'Редактировать лабораторную работу', 'error': ''}
    if request.method == "POST":
        form = EditTheoryForm(request.POST,request.FILES)
        form.fields["name"].widget.attrs["placeholder"] = f"Название работы: {theor.name}"
        form.fields["description"].widget.attrs["placeholder"] = f"Описание работы: {theor.description}"
        if form.is_valid():
            if form.data["name"]:
                theor.name= form.data["name"]
            if form.data["description"]:
                theor.description= form.data["description"]
            if request.FILES:
                theor.file = request.FILES["file"]
            theor.save()
            url = '/all_theory/theory/' + str(theor.id)
            return redirect(url)
        else:
            context["error"] = "Введенные данные не соответствуют формату"
        context["form"] = form
    else:
        form = EditTheoryForm(request.POST,request.FILES)
        form.fields["name"].widget.attrs["placeholder"] = f"Название работы: {theor.name}"
        form.fields["description"].widget.attrs["placeholder"] = f"Описание работы: {theor.description}"
        context['form'] = form
    return render(request, "theory_changer.html", context)
@xframe_options_exempt
def sim(request: HttpRequest):
    context = {}
    return render(request,"circuitjs1/war/circuitjs.html",context)