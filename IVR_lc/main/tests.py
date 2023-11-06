from django.test import TestCase, Client
from django.contrib.auth.models import User
class ProjTest(TestCase):
    def setUp(self):
        """Получение тестового клиента"""
        self.client = Client()
        self.credentials = {
            'username': 'test1',
            'password': 'testtest',
        }
        User.objects.create_user(**self.credentials)
    def test_index(self):
        """
        Проверка работы главной страницы
        """
        response = self.client.get("/")
        self.assertEqual(response.status_code,200)
    def test_login(self):
        """
        Проверка работы страницы авторизации
        """
        response = self.client.get("/login/")
        self.assertEqual(response.status_code, 200)
    def test_pwd_reset(self):
        """
        Проверка работы страницы рабочего стола
        без учетной записи
        """
        response = self.client.get("/password_reset/")
        self.assertEqual(response.status_code, 200)
    def test_auth(self):
        """
        Проверка работы страницы регистрации
        """
        response = self.client.get("/registration/")
        self.assertEqual(response.status_code, 200)
    def test_th_create(self):
        """
        Проверка работы страницы создания лабораторной работы
        """
        response = self.client.get("/create/")
        self.assertEqual(response.status_code, 200)
    def test_email(self):
        """
        Проверка работы страницы
        """
        response = self.client.get("/email_enter/")
        self.assertEqual(response.status_code, 200)

# Create your tests here.
