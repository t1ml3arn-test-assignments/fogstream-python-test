from django.test import TestCase, SimpleTestCase
from django.contrib.auth.models import User
from django.urls import reverse

# Create your tests here.

class RegisterViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(username='user1', password='123')

    def setUp(self):
        self.client.logout()

    # --------------------------------

    def test_redirect_to_send_msg_if_logged_in(self):
        login = self.client.login(username='user1', password='123')
        self.assertTrue(login, "Can't login user1 with pass 123")

        response = self.client.get(reverse('register'))
        self.assertRedirects(response, reverse('sendmsg'))

    def test_no_redirect_if_anon(self):
        # this also tests if url with name "register" exists
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)

    def test_view_url_exist(self):
        # this also tests if url name "register" exists
        response = self.client.get('/register/')
        self.assertEqual(response.status_code, 200)

    def test_template_exist(self):
        response = self.client.get(reverse('register'))
        self.assertTemplateUsed(response, 'register.html')

    def test_redirect_if_register_succeeded(self):
        passw = "!12345678"
        response = self.client.post(reverse('register'), {"username": "user2", "password1": passw, "password2": passw})
        self.assertRedirects(response, reverse('sendmsg'))

class LoginViewTest(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(username='user1', password='123')

    def setUp(self):
        self.client.logout() 

    # ------------------------------------------------

    def test_template_exist(self):
        response = self.client.get(reverse('login'))
        self.assertTemplateUsed(response, 'login.html')

    def test_view_url_name_exist(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_view_url_exist(self):
        response = self.client.get('/login/')
        self.assertEqual(response.status_code, 200)

    def test_redirect_if_already_logged_in(self):
        login = self.client.login(username='user1', password='123')
        self.assertTrue(login, "Cant login")

        response = self.client.get(reverse('login'))
        self.assertRedirects(response, reverse('sendmsg'))

    def test_redirect_if_login_succeeded(self):
        response = self.client.post(reverse('login'), {"username": "user1", "password": "123"})
        self.assertRedirects(response, reverse('sendmsg'))

class EmptyUrlRedirectTest(SimpleTestCase):

    def test_redirect_to_register(self):
        response = self.client.get("")
        self.assertRedirects(response, reverse("register"))