from django.test import TestCase, override_settings
from django.contrib.auth.models import User
from django.urls import reverse
import datetime
from send_msg.views import send_msg
from send_msg.models import Message

class SendMsgViewTest(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(username='user1', password='123')
        User.objects.create_user(username='user2', password='123', email='username@google.com')
        User.objects.create_user(username='admin', password='123', email='admin@mail.com', is_staff=True)
    
    def tearDown(self):
        self.client.logout()

    def test_login_required(self):
        response = self.client.get(reverse('sendmsg'))
        self.assertRedirects(response, '/login/?next=/send-message/')
    
    def test_no_redirect_if_logged_in(self):
        login = self.client.login(username='user1', password='123')
        self.assertTrue(login, "Can't login")

        response = self.client.get(reverse('sendmsg'))
        self.assertEqual(response.status_code, 200)

    def test_template_exist(self):
        login = self.client.login(username='user1', password='123')
        self.assertTrue(login, "Can't login")

        response = self.client.get(reverse('sendmsg'))
        self.assertTemplateUsed(response, 'send-message.html')

    def test_view_url_exist(self):
        response = self.client.get('/send-message/')
        # redirect or success (not a good idea ?)
        self.assertIn(response.status_code, [302, 200])
    
    def test_view_url_name_exist(self):
        # test if an url name exists
        response = self.client.get(reverse('sendmsg'))
        self.assertIn(response.status_code, [302, 200])

    def test_redirect_to_send_msg_on_success_submit(self):
        login = self.client.login(username='user1', password='123')
        self.assertTrue(login, "Can't login")
        
        response = self.client.post(reverse('sendmsg'), {"receiver": "admin@mail.com", "text": "hello"})
        self.assertRedirects(response, reverse('sendmsg'))

    def test_updating_message_model(self):
        login = self.client.login(username='user1', password='123')
        self.assertTrue(login, "Can't login")

        admin_email = "admin@mail.com"
        self.client.post(reverse('sendmsg'), {"receiver": admin_email, "text": "hello"})
        msg = Message.objects.get(receiver=admin_email)
        self.assertEqual(msg.receiver, admin_email)
        self.assertEqual(msg.text, "hello")
        self.assertEqual(msg.success, True)
        self.assertEqual(msg.sender, User.objects.get(id=1))
        # at least we can check if dates are the same (with no time info)
        # date must be present and that is enough
        self.assertEqual(msg.date.date(), datetime.date.today())
        
        msg.delete()

    @override_settings(EMAIL_BACKEND='django.core.mail.backends.base.BaseEmailBackend')
    def test_msg_was_not_sent(self):
        # to simulate email sending error just use BaseEmailBackend
        login = self.client.login(username='user1', password='123')
        self.assertTrue(login, "Can't login")

        admin_email = "admin@mail.com"
        self.client.post(reverse('sendmsg'), {"receiver": admin_email, "text": "hello"})
        msg = Message.objects.get(receiver=admin_email)
        self.assertFalse(msg.success)
    