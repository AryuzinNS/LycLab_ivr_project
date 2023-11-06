from django import forms

class RegForm(forms.Form):
    """Форма регистрации пользователя
    :variable CHOICES: Категории доступа
    :param username: Логин пользователя
    :param frst_name: Имя
    :param last_name: Фамилия
    :param email: Адрес электронной почты пользователя
    :param password: Пароль
    :param sec_password: Второй пароль(подтверждение)
    :param is_teacher: Категория доступа
    """
    CHOICES = [
        (1, "Учитель"),
        (0, "Студент"),
    ]
    username = forms.CharField(label="Логин", required=True , widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Введите ваш логин',
    }))
    frst_name = forms.CharField(label="Имя", required=True,widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Введите ваше имя',
    }))
    last_name = forms.CharField(label="Фамилия", required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Введите вашу фамилию',
    }))
    email = forms.EmailField(label="Email", required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Введите ваш email',
    }))
    password = forms.CharField(label="Пароль", min_length=5, max_length=30, required=True,
                               widget=forms.PasswordInput(attrs={
                                   'class': 'form-control',
                                   'placeholder': 'Введите пароль',
                               }))
    sec_password = forms.CharField(label="Повторите пароль", required=True, min_length=8, max_length=30,
                                   widget=forms.PasswordInput(attrs={
                                       'class': 'form-control',
                                       'placeholder': 'Введите пароль ещё раз',
                                   }))
    is_teacher = forms.IntegerField(label="Выберите тип пользователя", required=True,
                                    widget=forms.RadioSelect(choices=CHOICES, attrs={
                                        'class': 'form-check-inline',
                                    }))


class LoginForm(forms.Form):
    """
    Форма входа

    :param username: Получаем логин/юзернейм (CharField)
    :param password: Получаем пароль (CharField)
    """
    username = forms.CharField(label="Имя пользователя", required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Введите ваш юзернейм',
    }))
    password = forms.CharField(label="Пароль", required=True, widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Введите пароль',
    }))


class AddTheoryForm(forms.Form):
    """
    Форма добавления теоретических материалов

    :param name: Название работы
    :param description: Описание работы
    :param file: Файл теоретических материалов работы
    """
    name = forms.CharField(label="Название работы:", min_length=1, required=True, widget=forms.TextInput(attrs={
        'class': 'form-control  w-100 mb-3',
        'placeholder': 'Введите название работы',
    }))
    description = forms.CharField(label="Тема работы:", min_length=5, required=True,
                                  widget=forms.Textarea(attrs={
                                      'class': 'form-control w-100 mb-3',
                                      'placeholder': 'Опишите тему работы',
                                  }))
    file = forms.FileField(label="Теоретические материалы:", required=True, widget=forms.FileInput(attrs={
        'class': "form-control mb-3 ",
        'placeholder': 'Прикрепите файл с теорией',
    }))


class ProfEditForm(forms.Form):
    """
    Форма редактирования профиля
    :param username: username
    :param first_name: имя пользователя
    :param last_name: Фамилия пользователя
    :param email: Адрес электронной почты
    :param age: Возраст пользователя
    :param password: пароль
    :param sec_password: подтверждение пароля
    """
    username = forms.CharField(label="Логин", required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
    }))
    first_name = forms.CharField(label="Имя", required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
    }))
    last_name = forms.CharField(label="Фамилия", required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
    }))
    email = forms.EmailField(label="Email", required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
    }))
    age = forms.IntegerField(label="Возраст", required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
    }))
    password = forms.CharField(label="Пароль", min_length=8, max_length=30, required=True, widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': "Введите пароль"
    }))
    sec_password = forms.CharField(label="Повторите пароль", min_length=8, max_length=30, required=True, widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': "Введите пароль еще раз"
    }))


class EditTheoryForm(forms.Form):
    """
    Форма изменения теоретических материалов

    :param name: Название работы
    :param description: Описание работы
    :param file: Файл теоретических метериалов работы
    """
    name = forms.CharField(label="Введите название работы", min_length=1, required=False, widget=forms.TextInput(attrs={
        'class': 'form-control  w-100 mb-3',
    }))
    description = forms.CharField(label="Опишите тему работы", min_length=5, required=False,
                                  widget=forms.Textarea(attrs={
                                      'class': 'form-control w-100 mb-3',
                                  }))
    file = forms.FileField(label="Теоретические материалы:", required=False, widget=forms.FileInput(attrs={
        'class': "form-control mb-3 ",
    }))


class SearchPrForm(forms.Form):
    """
    Форма поиска теоретических материалов
     :param text: Текст поискового запроса
    """
    text = forms.CharField(min_length=1, required=False, widget=forms.TextInput(attrs={
        "class": "form-control border border-right-",
        "id": "search_label",
        "placeholder": "Искать проекты...",

    }))


class EnterMailForm(forms.Form):
    """
        Форма поиска теоретических материалов
         :param email: Адрес электронной почты
        """
    email = forms.EmailField(label="Введите адрес электронной почты", min_length=8, required=True,
                             widget=forms.TextInput(attrs={
                                 'class': 'form-control',
                                 'placeholder': "Введите адрес электронной почты"
                             }))


class ResetPasswordCode(forms.Form):
    """
        Форма изменения теоретических материалов

        :param login: Логин пользователя
        :param password: Пароль пользователя
        :param sec_password: Второй пароль для подтвержидения
        :param code: Код подтверждения из почты
    """
    login = forms.CharField(label="Логин", required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': "Введите логин"
    }))
    password = forms.CharField(label="Пароль", min_length=8, max_length=30, required=True,
                               widget=forms.PasswordInput(attrs={
                                   'class': 'form-control',
                                   'placeholder': "Введите пароль"
                               }))
    sec_password = forms.CharField(label="Повторите пароль", min_length=8, max_length=30, required=True,
                                   widget=forms.PasswordInput(attrs={
                                       'class': 'form-control',
                                       'placeholder': "Введите пароль еще раз"
                                   }))
    code = forms.CharField(label="Код из сообщения", required=True, widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': "Введите код из сообщения"
    }))
