from django.test import TestCase
from django.contrib.auth.models import User
from send_msg.models import Message
import datetime

def get_msg(id):
    return Message.objects.get(id=id)

class MessageModelTest(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        user1 = User.objects.create_user(username='user1', password='!12345678')
        user1.save()

        Message.objects.create(text="hello", receiver="admin@mail.com", success=True, date=datetime.datetime.now(), sender=None)
        Message.objects.create(text="hello again", receiver="admin@mail.com", success=True, date=datetime.datetime.now(), sender=user1)

    def test_message_max_len(self):
        msg = Message.objects.get(id=1)
        max_len = msg._meta.get_field('text').max_length
        self.assertEqual(max_len, 1000)

    def test_mail_max_len(self):
        msg = Message.objects.get(id=1)
        max_len = msg._meta.get_field('receiver').max_length    
        self.assertEqual(max_len, 254)
    
    def test_sender_fk(self):
        m1 = get_msg(1)
        m2 = get_msg(2)
        self.assertIsNone(m1.sender)
        self.assertEqual(m2.sender, User.objects.get(id=1))