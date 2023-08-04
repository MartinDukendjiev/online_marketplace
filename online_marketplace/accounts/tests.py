from django.test import TestCase, Client
from django.urls import reverse, reverse_lazy
from django.contrib.auth import get_user_model

UserModel = get_user_model()


class UserProfileTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = UserModel.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        self.profile_url = reverse('profile details', args=[self.user.pk])
        self.profile_edit_url = reverse('profile edit', args=[self.user.pk])
        self.profile_delete_url = reverse('profile delete', args=[self.user.pk])
        self.logout_url = reverse_lazy('login user')

    def test_profile_detail_view_authenticated(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/profile.html')

    def test_profile_detail_view_unauthenticated(self):
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/accounts/profile/{}/'.format(self.user.pk))

    def test_profile_update_view_authenticated(self):
        self.client.login(username='testuser', password='testpassword')
        new_data = {
            'first_name': 'New',
            'last_name': 'Name',
        }
        response = self.client.post(self.profile_edit_url, data=new_data)
        self.assertEqual(response.status_code, 302)
        updated_user = UserModel.objects.get(username='testuser')
        self.assertEqual(updated_user.first_name, 'New')
        self.assertEqual(updated_user.last_name, 'Name')

    def test_profile_update_view_unauthenticated(self):
        new_data = {
            'first_name': 'New',
            'last_name': 'Name',
        }
        response = self.client.post(self.profile_edit_url, data=new_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/accounts/profile/{}/edit/'.format(self.user.pk))

    def test_profile_delete_view_authenticated(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(self.profile_delete_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.logout_url)
        with self.assertRaises(UserModel.DoesNotExist):
            UserModel.objects.get(pk=self.user.pk)


class ProfileIntegrationTestCase(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        self.profile_url = reverse('profile details', args=[self.user.pk])
        self.login_url = reverse('login user')
        self.login_data = {'username': 'testuser', 'password': 'testpassword'}
        self.logout_url = reverse('logout user')
        self.invalid_login_data = {'username': 'invaliduser', 'password': 'invalidpassword'}
        self.comment_data = {'content': 'Test comment'}
        self.rating_data = {'rating_value': 5}

    def test_successful_login_redirect(self):
        response = self.client.post(self.login_url, data=self.login_data, follow=True)
        self.assertRedirects(response, reverse('index'))

    def test_unsuccessful_login_display_error(self):
        response = self.client.post(self.login_url, data=self.invalid_login_data)
        self.assertContains(response,
                            'Please enter a correct username and password. Note that both fields may be case-sensitive.')

    def test_successful_logout_redirect(self):
        login_response = self.client.post(self.login_url, data=self.login_data, follow=True)
        self.assertEqual(login_response.status_code, 200)
        response = self.client.get(self.logout_url, follow=True)
        self.assertRedirects(response, reverse('login user'))

    def test_add_comment(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(self.profile_url, data=self.comment_data, follow=True)
        self.assertEqual(response.status_code, 200)

    def test_add_rating_and_display_on_profile_page(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(self.profile_url, data=self.rating_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '5')
