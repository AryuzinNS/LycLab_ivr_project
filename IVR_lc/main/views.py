# Установка требуемых библиотек и функций Джанго
from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
# Импорт форм
from main.forms.forms import RegForm, LoginForm, AddTheoryForm, ProfEditForm, EditTheoryForm, SearchPrForm, \
    EnterMailForm, ResetPasswordCode
# Импорт моделей
from main.models import Profile, Theory, TheorySearcher
# Установка требуемых библиотек и функций Джанго
from django.http.request import HttpRequest
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.views.decorators.clickjacking import xframe_options_exempt
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import random
# Установка требуемых библиотек для работы с электронной почтой
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def index_page(request: HttpRequest):
    """Обработчик главной страницы
    :param request- Запрос пользователя
    :return -  Возвращение  главной страницы
    """
    # Создание словаря обмена с html
    context = {}
    context['author'] = 'Aryuzin Nikita'
    # Создание словаря обмена с html
    if auth.get_user(request).is_authenticated:
        # Получение идентификатора пользователя
        id = get_user_id(request)
        prof = Profile.objects.get(id=id)
        # ДОбавление данных в словарь
        context['id'] = id
        context['fullname'] = prof.fullname
    # Обработка шаблона
    return render(request, 'index.html', context)


def get_user_id(request: HttpRequest):
    """
    Получение ID текущего пользователя

    :param request: Запрос пользователя
    :return: ID текущего пользователя
    """
    if auth.get_user(request).id:
        return int(auth.get_user(request).id)


def validateEmail(email):
    """
    Функция валидации адреса эл. почты
    param email- Электронный адрес для проверки
    """
    try:
        validate_email(email)
        return True
    except ValidationError:
        return False
def registration_page(request: HttpRequest):
    """
    Страница регистрации пользователя

    :param request: Запрос пользователя
    :return: Возвращает страницу
    """
    # Создание словаря обмена с html
    context = {'pagename': 'Регистрация', 'error': ''}
    # Обработка запроса
    if request.method == "POST":
        # Создание форма
        form = RegForm(request.POST)
        # Проверка формата формы
        if form.is_valid():
            # Проверка адреса электронной почты
            if validateEmail(form.data["email"]):
                # Проверить совпадение пароля
                if form.data["password"] == form.data["sec_password"]:
                    # Проверка формата юзернейма
                    checkstr = form.data["username"]
                    if checkstr.isdigit():
                        context["error"] = "Юзернейм должен содержать хотя бы одну букву"
                    else:
                        # Проверка формата имени
                        if form.data["frst_name"].isalpha():
                            # Проверка формата фамилии
                            if form.data["last_name"].isalpha():
                                # Получение записи пользователя
                                user1 = User.objects.filter(username=form.data["username"])
                                # Проверка на уникальность логина
                                if not user1:
                                    # Создание записи пользователя
                                    user = User(username=form.data["username"],
                                                first_name=form.data["frst_name"],
                                                last_name=form.data["last_name"],
                                                email=form.data["email"])
                                    user.set_password(form.data['password'])
                                    # Сохранение записи пользователя в БД
                                    user.save()
                                    # Создание и сохранение записи профиля в БД
                                    fullname = form.data["frst_name"] + " " + form.data["last_name"]
                                    new_profile = Profile(fullname=fullname,
                                                          age=21,
                                                          isteacher=form.data["is_teacher"],
                                                          user=user)
                                    new_profile.save()
                                    # Аутентификация пользователя
                                    user = authenticate(username=form.data["username"], password=form.data["password"])
                                    # Вход в профиль
                                    login(request, user)
                                    # Перенаправление на страницу информации о профиле
                                    url = '/profile/' + str(get_user_id(request))
                                    return redirect("/")
                                else:
                                    context["error"] = "Фамилия пользователя должна содержать только буквы"
                            else:
                                context["error"] = "Имя пользователя должно содержать только буквы"
                        else:
                            context["error"] = "Этот юзернейм уже занят! Но Вы всегда можете выбрать другой"
                else:# Обработка ошибок
                    context["error"] = "Введенные пароли не совпадают"
                    context['form'] = RegForm(request.POST)
        context["form"] = form
    else:
        context['form'] = RegForm(request.POST)
    return render(request, 'registration.html', context)


def login_page(request: HttpRequest):
    """
    Страница логина

    :param request: Запрос пользователя
    :return: Страница входа в профиль пользователя
    """
    # Создание словаря-обменника с html
    context = {'user_id': get_user_id(request), "pagename": 'Авторизация'}
    # Обработка запроса пользователя
    if request.method == "GET":
        # Создание формы
        form = LoginForm()
        context['form'] = form
        # Проверка авторизован ли пользователь
        if auth.get_user(request).is_authenticated:
            return redirect('/')
    # Обработка запроса пользователя
    if request.method == "POST":
        # Проверка авторизован ли пользователь
        if auth.get_user(request).is_authenticated:
            return redirect('/')
        # Создание формы
        form = LoginForm(request.POST)
        # Проверка формата формы
        if form.is_valid():
            # Создание записи пользователя
            context['form'] = form
            user = authenticate(username=form.data["username"], password=form.data["password"])
            # Аутентификация пользователя
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
    # Выход из профиля пользователя
    auth.logout(request)
    return redirect('/')


@login_required(login_url="/login")
def profile_page(request: HttpRequest, id=-1):
    """
    Создаёт и возвращает страницу профиля пользователя.

    :param request: Запрос пользователя
    :return: Страница профиля пользователя
    """
    # Получение ID-пользователя
    if id == -1:
        id = get_user_id(request)
    # Получение данных из БД о пользователе
    prof = Profile.objects.get(id=id)
    user = User.objects.get(id=id)
    # Создание словаря отображения в html
    context = {
        'name': prof.fullname,
        'login': user.username,
        'email': user.email,
        'age': prof.age,
        'id': id,
        'pagename': "Профиль",
    }
    return render(request, "profile.html", context)

@login_required(login_url="/login")
@xframe_options_exempt
def verstak(request: HttpRequest):
    """"
    Создает и возвращает страницу интерактивной доски
    :param request: Запрос пользователя
    :return: Страница интерактивной лаборатории
    """
    # Аутентификация пользователя
    context = {
        "datetime": datetime.now(),
    }
    # Сохранение в контекст пользователя из запроса
    if request.user:
        context["user"] = request.user
    # Обработка страницы
    return render(request, "workbench.html", context)


@xframe_options_exempt
def all_theory(request: HttpRequest):
    """Создает и возвращает страницу всех теоретических материалов
    :param request: Запрос пользователя
    :return: Страница с перечнем лабораторных работ
    """
    # Получение записи профиля
    id = get_user_id(request)
    prof = Profile.objects.get(id=id)
    # Получение массивов имен, описаний, авторства из поисковой бд
    names = [work.name for work in TheorySearcher.objects.all()]
    descriptions = [work.description for work in TheorySearcher.objects.all()]
    bys = [work.by for work in TheorySearcher.objects.all()]
    # Создание перечня работ
    works = []
    rq = ""
    # Обработка запроса пользователя
    if request.method == "POST":
        # Создание формы
        frm = SearchPrForm(request.POST)
        # Проверка формата формы
        if frm.is_valid():
            # Проверка наличия поискового запроса
            if frm.data["text"]:
                # Поиск по созданным массивам(регистронезависимый)
                rq = frm.data["text"].lower()
                for i in range(len(names)):
                    # Проверка по названиям
                    if rq in names[i]:
                        obj = TheorySearcher.objects.get(name=names[i])
                        object = Theory.objects.get(id=obj.theory_id)
                        works.append({object: Profile.objects.get(id=object.user_id).fullname})
                    # Проверка по описаниям
                    elif rq in descriptions[i]:
                        obj = TheorySearcher.objects.get(description=descriptions[i])
                        object= Theory.objects.get(id=obj.theory_id)
                        works.append({object:Profile.objects.get(id= object.user_id).fullname})
                    # Проверка по авторству
                    elif rq in bys[i]:
                        obj = TheorySearcher.objects.get(by=bys[i])
                        object= Theory.objects.get(id=obj.theory_id)
                        works.append({object:Profile.objects.get(id= object.user_id).fullname})
            else:
                # Создание массива работ
                works = [{object : Profile.objects.get(id=object.user_id).fullname} for object in Theory.objects.all()]
    else:
        # Создание формы
        frm = SearchPrForm(request.POST)
        works = [{object : Profile.objects.get(id=object.user_id).fullname} for object in Theory.objects.all()]
    # Создание словаря для отображения html страницы
    context = {
        "datetime": datetime.now(),
        "pagename": "Теоретические материалы",
        "works": works,
        "isteacher": False,
        "form": frm,
    }
    # Проверка уровня доступа пользователя
    if prof.isteacher == 1:
        context["isteacher"] = True
    return render(request, "all_theory.html", context)


def reset_filter(request: HttpRequest):
    # Создание формы
    frm = SearchPrForm(request.POST)
    # Создание массива работ
    works = [{object : Profile.objects.get(id=object.user_id).fullname} for object in Theory.objects.all()]
    # Создание словаря для отображание html страницы
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
    # Получение ID пользователя
    id1 = get_user_id(request)
    # Получение данных профиля
    prof = Profile.objects.get(id=id1)
    work = Theory.objects.get(id=id)
    # Получение данных профиля
    prf = Profile.objects.get(id=work.user_id)
    usr = User.objects.get(id=work.user_id)
    # Создание словаря для отображения в html
    context = {
        'id': work.id,
        'title': work.name,
        'description': work.description,
        'file': work.file,
        "by": prf.fullname,
        "email": usr.email,
        "isteacher": False,
    }
    # Проверка доступа пользователя
    if prof.isteacher == 1:
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
    #Проверка метода запроса
    if request.method == "POST":
        # Создание формы
        form = AddTheoryForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES["file"].name
            # Проверка формата файла
            if not True:#(not file.endswith('.pdf')) or (not file.endswith('.doc')) or (not file.endswith('.docx')):
                context["error"] = "Файл с теорией должен быть расширения .pdf, .doc, .docx"
            else:
                # Проверка формата названия
                if form.data["name"].isdigit():
                    context["error"] = "Название работы должно содержать буквы"
                else:
                    # Проверка формата описания
                    if form.data["description"].isdigit():
                        context["error"] = "Описание работы должно содержать буквы"
                    else:
                        # Сохранение данных теории для отображения
                        user = auth.get_user(request)
                        prof = Profile.objects.get(id=user.id)
                        new_theory = Theory(name=form.data["name"], description=form.data["description"],
                                            user_id=auth.get_user(request).id)
                        new_theory.file = request.FILES["file"]
                        new_theory.save()
                        id = new_theory.id
                        """
                        Создание зеркального объекта для поиска
                        """
                        theory_mirror = TheorySearcher(name=form.data["name"].lower(),
                                                       description=form.data["description"].lower(),
                                                       by=prof.fullname.lower(),
                                                       email=user.email,
                                                       theory_id=id)
                        theory_mirror.save()
                        url = '/all_theory/theory/' + str(id)
                        return redirect(url)
        else:
            context["error"] = "Введенные данные не соответствуют формату"
        context["form"] = form
    else:
        # Иначе: отобразить пустую форму
        context['form'] = AddTheoryForm(request.POST, request.FILES)
    return render(request, 'theory_editor.html', context)


@login_required(login_url="/login")
def profile_editor(request: HttpRequest, id=-1):
    """
    Создает и возвращает страницу редактирования профиля пользователя
    :param request: Запрос пользователя
    :return: страница редактора профиля пользователя
    """
    # Получение записей пользователя
    id = get_user_id(request)
    prof = Profile.objects.get(id=id)
    user = User.objects.get(id=id)
    context = {'pagename': 'Редактировать профиль', 'error': ''}
    if request.method == "POST":
        # Создание формы пользователя и получение полного имени пользователя для плейсхолдеров
        form = ProfEditForm(request.POST)
        fullname = prof.fullname.split(' ')
        #Проверка формата полного имени для плейсхолдера
        if len(fullname) == 2:
            form.fields["last_name"].widget.attrs["placeholder"] = f"Фамилия: {fullname[1]}"
        else:
            form.fields["last_name"].widget.attrs["placeholder"] = "Фамилия: "
        # Установка плейсхолдеров
        form.fields["username"].widget.attrs["placeholder"] = f"Логин: {user.username}"
        form.fields["email"].widget.attrs["placeholder"] = f"Email: {user.email}"
        form.fields["first_name"].widget.attrs["placeholder"] = f"Имя: {prof.fullname[0]}"
        form.fields["age"].widget.attrs["placeholder"] = f"Возраст: {prof.age}"
        if form.is_valid():
            #Проверка формата юзернейма
            if form.data["username"].isdigit():
                context["error"] = "Юзернейм должен содержать хотя бы одну букву"
            else:
                # Проверка формата имени
                if not str(form.data["first_name"]).isalpha():
                    context["error"] = "Имя должно состоять только из букв"
                else:
                    # Проверка формата фамилии
                    if (form.data["last_name"]).isalpha():
                        # Проверка совпадения паролей
                        if form.data["password"] == form.data["sec_password"]:
                            # Проверка валидности электронной почты
                            if validateEmail(form.data["email"]):
                                # Проверка формата возраста
                                if form.data["age"].isdigit():
                                    # Изменение данных пользователя
                                    user.username = form.data["username"]
                                    user.set_password(form.data["password"])
                                    prof.fullname = form.data["first_name"] + " " + form.data["last_name"]
                                    user.first_name = form.data["first_name"]
                                    user.last_name = form.data["last_name"]
                                    user.email = form.data["email"]
                                    prof.age = form.data["age"]
                                    prof.save()
                                    user.save()
                                    login(request, user)
                                    url = '/profile/' + str(prof.id)
                                    redirect("/")
                                    return redirect(url)
                                else:
                                    context["error"] = "Возраст может быть только числом"
                            else:
                                context["error"] = "Неверный формат ввода почты"
                        else:
                            context["error"] = "Введенные пароли не совпадают"
                    else:
                        context["error"] = "Фамилия должна состоять только из букв"
        else:
            context["error"] = "Введенные данные не соответствуют формату"
        context["form"] = form
    else:
        # Установка плейсхолдеров
        form = ProfEditForm(request.POST)
        fullname = prof.fullname.split(' ')
        form.fields["username"].widget.attrs["placeholder"] = f"Логин: {user.username}"
        form.fields["first_name"].widget.attrs["placeholder"] = f"Имя: {fullname[0]}"
        if len(fullname) == 2:
            form.fields["last_name"].widget.attrs["placeholder"] = f"Фамилия: {fullname[1]}"
        else:
            form.fields["last_name"].widget.attrs["placeholder"] = "Фамилия: "
        form.fields["email"].widget.attrs["placeholder"] = f"Email: {user.email}"
        form.fields["age"].widget.attrs["placeholder"] = f"Возраст: {prof.age}"
        context['form'] = form
    return render(request, "profeditor.html", context)


def edit_theory(request: HttpRequest, id=-1):
    """
    Страница редактирования теоретических материалов(Доступна только пользователям категории учитель)
    :param - Запрос пользователя
    :return - Возвращает страницу редактирования теоретических материалов
    """
    # Получение ID теоретических материалов по url адресу
    pth = request.get_full_path()[::-1][1:]
    id1 = ""
    i = 0
    while pth[i] != '/':
        id1+=pth[i]
        i+=1
    id1= id1[::-1]
    # Получение записи теоретических материалов
    theor = Theory.objects.get(id=int(id1))
    # Получение поискового зеркала теоретических материалов
    th_m = TheorySearcher.objects.get(theory_id = int(id1))
    context = {'pagename': 'Редактировать лабораторную работу', 'error': ''}
    # Обработка запроса
    if request.method == "POST":
        # Объявление формы
        form = EditTheoryForm(request.POST, request.FILES)
        # Установка плейсхолдеров
        form.fields["name"].widget.attrs["placeholder"] = f"Название работы: {theor.name}"
        form.fields["description"].widget.attrs["placeholder"] = f"Описание работы: {theor.description}"
        # Валидация формы
        if form.is_valid():
            # Проверка наличия данных для изменения
            # Проверка названия работы
            if form.data["name"]:
                # Сохранение названия в основной бд и зеркале для поиска
                theor.name = form.data["name"]
                th_m.name = form.data["name"].lower()
            # Проверка описания работы
            if form.data["description"]:
                # Сохранение описания в основной бд и зеркале для поиска
                theor.description = form.data["description"]
                th_m.description = form.data["description"].lower()
            # Проверка наличия файлов
            if request.FILES:
                # Получение имени файла
                file = request.FILES["file"].name
                # Проверка формата отправляемого файла из соображений безопасности
                if (not file.endswith('.pdf') )or (not file.endswith('.doc')) or (not file.endswith('.docx')) :
                    context["error"] = "Введенные данные не соответствуют формату"
                else:
                    # Запись файла в бд если прошел проверку на формат
                    theor.file = request.FILES["file"]
            # Сохранение теоретических материалов
            theor.save()
            th_m.save()
            # Перенаправление на адрес лабораторной работы
            url = '/all_theory/theory/' + str(theor.id)
            return redirect(url)
        else:
            context["error"] = "Введенные данные не соответствуют формату"
        # Отправка формы в обработчик
        context["form"] = form
    else:
        # Создание пустой формы с плейсхолдерами
        form = EditTheoryForm(request.POST, request.FILES)
        form.fields["name"].widget.attrs["placeholder"] = f"Название работы: {theor.name}"
        form.fields["description"].widget.attrs["placeholder"] = f"Описание работы: {theor.description}"
        context['form'] = form
    return render(request, "theory_changer.html", context)
# Генерация кода восстановления пароля
code =str(random.randint(10000,100000))
def email(address):
    """
    Функция отправляет сгенерированнный код на указанный адрес
    электронной почты
    param address - адрес электронной почты
    return - Возвращает сгенерированный и отправленный код для обработки следующей функцией
    """
    # Создание объект MIMEMultipart для сообщения
    msg = MIMEMultipart()
    # Установка темы сообщения
    msg['Subject'] = "Код для восстановления пароля:" + str(code)
    msg['From'] = "Виртуальная лаборатория LycLab"
    # Установка текста сообщения
    message = "Код для восстановления пароля:" + str(code)
    msg.attach(MIMEText(message, 'plain'))
    # Создание SMTP-соединения
    smtp_obj = smtplib.SMTP('smtp.gmail.com', 587)
    smtp_obj.starttls()
    # Вход в аккаунт gmail
    smtp_obj.login("Имя вашего гугл аккаунта", "Пароль к нему")
    # Отправка сообщения
    smtp_obj.sendmail("lol", address, msg.as_string())
    smtp_obj.quit()
    # Возвращение кода
    return str(code)
def EnterEmail(request: HttpRequest):
    """
    Функция отправки кода по Email в рамках смены пароля
    :param request: Запрос пользователя
    :return: возвращает страницу с формой для ввода адреса почты
    """
    # Создание словаря для отправки в html
    context = {'pagename': 'Редактировать лабораторную работу', 'error': ''}
    # Получение списка адресов
    addresses = [object.email for object in User.objects.all()]
    # Обработка запроса пользователя
    if request.method == "POST":
        # Создание формы
        form1 = EnterMailForm(request.POST)
        # Проверка формата формы
        if form1.is_valid():
            # Проверка наличия текста в форме
            if form1.data["email"]:
                # Проверка наличия адреса в БД
                if form1.data["email"] in addresses:
                    # Отправка кода по адресу
                    email(form1.data["email"])
                    return redirect("/password_reset/")
                else:
                    context["error"] = "Данный почтовый адрес не зарегистрирован в системе"
            else:
                context["frm1"] = form1
        else:
            context["error"] = "Неверный формат ввода"
    else:
        # Создание формы
        form1 = EnterMailForm(request.POST)
        context["frm1"] = form1
    return render(request, "restore_passwd.html", context)

def ResetPasswd(request:HttpRequest):
    """
    Функция смены пароля, если пользователь его забыл
    :param request: Запрос пользователя
    :return: возврщает страницу смены пароля
    """
    # Создание словаря отправки данных в html
    context = {'pagename': 'Изменить пароль', 'error': ''}
    # Создание списка логинов
    logins = [object.username for object in User.objects.all()]
    # Обработка запроса
    if request.method == "POST":
        # Создание формы
        form = ResetPasswordCode(request.POST)
        context["frm2"] = form
        # Проверка формата ввода
        if form.is_valid():
            # Проверка наличия юзернейма в системе
            if form.data["login"] in logins:
                # Получение записи пользователя
                user = User.objects.get(username=form.data["login"])
                # Проверка совпадения кода введенного пользователем с кодом отправленным по почне
                if form.data["code"] == str(code):
                    # Проверка совпадения паролей
                    if form.data["password"] == form.data["sec_password"]:
                        # Смена пароля
                        user.set_password(form.data["password"])
                        # Сохранение нового пароля
                        user.save()
                        return redirect("/login/")
                    else:
                        context["error"] = "пароли не совпадают"
                else:
                    context["error"] = "Код не совпадает с отправленным"
            else:
                context["error"] = "Пользователь с данным логином не зарегистрирован в системе"
        else:
            context["error"] = "Неверный формат ввода"
    else:
        # Создание формы
        form = ResetPasswordCode(request.POST)
    # Отправка формы в контекст
    context["frm2"] = form
    return render(request, "edit_passwd.html", context)
