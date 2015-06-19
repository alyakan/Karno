from django.test import TestCase
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from main.models import YoutubeUrl


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


class YoutubeUrlTestCase(TestCase):
    """
    Tests YoutubeUrl model

    Author: Aly Yakan
    """
    def test_access_add_url_page_not_signed_in(self):
        """
        Redirects to login for guests trying to embed a youtube video

        Author: Aly Yakan
        """
        response = self.client.get(
            reverse('youtubeurl-add'))
        self.assertRedirects(
            response, '/main/user/login/?next=/main/add/youtubeurl/')

    def test_access_add_url_page_signed_in(self):
        """
        Results true for users trying to access the page for embedding
        Youtube videos

        Author: Aly Yakan
        """
        User.objects.create_user(username='johndoe', password='123456')
        response = self.client.post(
            reverse('user-login'),
            {'username': u'johndoe', 'password': '123456'})
        self.assertEqual(response.status_code, 302)
        response = self.client.get(
            reverse('youtubeurl-add'))
        self.assertEqual(response.status_code, 200)

    def test_add_url(self):
        """
        Results true for users embedding
        Youtube videos

        Author: Aly Yakan
        """
        User.objects.create_user(username='johndoe', password='123456')
        response = self.client.post(
            reverse('user-login'),
            {'username': u'johndoe', 'password': '123456'})
        self.assertEqual(response.status_code, 302)
        response = self.client.post(
            reverse('youtubeurl-add'),
            {'url': 'https://www.youtube.com/watch?v=AdSdsdaZel8'})
        self.assertRedirects(
            response, reverse('youtube_video_list'))
        urls = YoutubeUrl.objects.all().count()
        self.assertEqual(urls, 1)
