from django.shortcuts import redirect
from django.test import TestCase
from .models import User
# Create your tests here.


class UserModelTests(TestCase):
    def setUp(self):
        User.objects.create(username='alice')

    def test_user_default_auth_state(self):
        alice = User.objects.get(username='alice')
        self.assertEqual(alice.is_auth, False)


class UserViewCallTests(TestCase):
    list_url = '/user/list/'
    redirect_url = '/user/login/?next=/user/list/'

    def setUp(self):
        User.objects.create_user(username="alice", password='password')

    def test_call_list_view_deny_anonymous(self):
        response = self.client.get(self.list_url, follow=True)
        self.assertRedirects(response, self.redirect_url)

    def test_call_list_view_load(self):
        self.client.login(username='alice', password='password')
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user_list.html')
