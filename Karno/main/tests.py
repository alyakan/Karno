from django.test import TestCase
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse


class Authentication(TestCase):
    """
    Class to test Authentication system
    Author: Moustafa
    """
    def test_sign_up_correct_info(self):
        """
        Tests user sign up with correct info and matching passwords
        Author: Moustafa
        """
        response = self.client.post(
            reverse('user-new'), {'username': 'mostafa',
                                  'password1': 'thekey',
                                  'password2': 'thekey'})
        print response
        self.assertTrue(User.objects.get(username='mostafa'))
        self.assertRedirects(response, reverse('home'))

    def test_sign_up_missmatcing_password(self):
        """
        Tests user sign up with missmatching passwords
        Author: Moustafa
        """
        self.client.post(
            reverse('user-new'), {'username': 'mostafa',
                                  'password1': 'thekey',
                                  'password2': 'keythe'})
        self.assertFalse(User.objects.filter(username='mostafa'))

    def test_change_password(self):
        """
        Test User's ability to change password
        Author: Moustafa
        """
        self.client.post(
            reverse('user-new'), {'username': 'mostafa',
                                  'password1': 'thekey',
                                  'password2': 'thekey'})
        self.client.post(
            reverse('user-change-password'), {'old_password': 'thekey',
                                              'new_password1': 'pass',
                                              'new_password2': 'pass'})
        response = self.client.login(username='mostafa', password='pass')
        self.assertTrue(response)
