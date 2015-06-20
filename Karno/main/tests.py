from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from main.models import YoutubeUrl, GroupPermission, File
from django.core.files.uploadedfile import SimpleUploadedFile


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


class FileUploadTestCase(TestCase):

    """
    Class to Test File upload
    Author: Rana El-Garem
    """

    def setUp(self):
        self.client = Client()
        User.objects.create_user(username='rana',
                                 password='123456')
        self.client.post(reverse('user-login'),
                         {'username': 'rana',
                          'password': '123456'})

    def test_user_must_be_logged_in(self):
        """
        Checks redirection to login page
        when user requests upload page and is not logged in
        Author: Rana El-Garem

        """
        self.client.get(reverse('user-logout'))
        response = self.client.get(reverse('upload'))
        self.assertEqual(response.status_code, 302)

    def test_file_upload(self):
        """
        Ensures File instance created
        Author: Rana El-Garem
        """
        uploadedfile = SimpleUploadedFile(
            "file.mp4",
            "file_content",
            content_type="video/mp4")

        response = self.client.post(reverse('upload'),
                                    {
                                    'file_uploaded': uploadedfile,
                                    'user':
                                    self.client.session['_auth_user_id']
                                    })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(File.objects.count(), 1)

    def test_file_does_not_exist(self):
        """
        Ensures File must be provided for upload
        Author: Rana El-Garem
        """
        response = self.client.post(reverse('upload'),
                                    {
            'user': self.client.session['_auth_user_id']
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(File.objects.count(), 0)

    def test_permission_group(self):
        """
        Ensures GroupPermission Instance Created
        Author: Rana El-Garem
        """
        uploadedfile = SimpleUploadedFile(
            "file.mp4",
            "file_content",
            content_type="video/mp4")
        init_group_permission = GroupPermission.objects.count()
        response = self.client.post(reverse('upload'),
                                    {
                                    'file_uploaded': uploadedfile,
                                    'user':
                                    self.client.session['_auth_user_id'],
                                    'group': 1,
                                    'users': [u'1']
                                    })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(GroupPermission.objects.count(),
                         init_group_permission + 1)

    def test_ensure_group_is_set(self):
        """
        Ensures GroupPermission Instance is Created
        only when attribute group is set
        Author: Rana El-Garem
        """
        uploadedfile = SimpleUploadedFile(
            "file.mp4",
            "file_content",
            content_type="video/mp4")
        init_group_permission = GroupPermission.objects.count()
        response = self.client.post(reverse('upload'),
                                    {
                                    'file_uploaded': uploadedfile,
                                    'user':
                                    self.client.session['_auth_user_id'],
                                    'users': [u'1']
                                    })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(GroupPermission.objects.count(),
                         init_group_permission)





