from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from send_msg.models import Message
from send_msg.forms import SendMessageModelForm
import datetime

def get_msg(id):
    return Message.objects.get(id=id)

class SendMessageModelFormTest(TestCase):
    
    @classmethod
    def setUpTestData(cls):

        # create staff user
        User.objects.create_user(username='admin', password='!12345678', email='admin@mail.com', is_staff=True)
        User.objects.create_user(username='user', password='123', email='user@mail.com', is_staff=False)
        
    def test_labels(self):
        # fields in that form have different labels
        form = SendMessageModelForm()
        self.assertEqual(form.fields['receiver'].label, "Admin's email")
        self.assertEqual(form.fields['text'].label, "Message")
    
    def test_fields(self):
        # form doesnt have all fields from Message model
        form = SendMessageModelForm()
        fields = form.fields
        self.assertEqual(2, len(fields))
        self.assertTrue('text' in fields)
        self.assertTrue('receiver' in fields)

    def test_clean_receiver(self):

        # good case - form gets email which exists in db
        admin_email = "admin@mail.com"
        form = SendMessageModelForm(data={"receiver": admin_email})
        form.is_valid()

        clean_receiver = form.clean_receiver()
        self.assertEqual(admin_email, clean_receiver)
        
        # bad case - forms gets email which doesnt exist in db
        form = SendMessageModelForm(data={"receiver": "hello@world.com"})
        form.is_valid()
        with self.assertRaises(ValidationError):
            form.clean_receiver()
    
    def test_receiver_is_not_staff(self):
        # msg can be sent only to staff

        user_email = 'user@mail.com'
         
        form = SendMessageModelForm(data={"receiver": user_email})
        form.is_valid()
        with self.assertRaises(ValidationError):
            form.clean_receiver()

    # NOTE both test_clean_receiver() test_receiver_is_not_staff
    # can be simplified by using simple form.is_valid()