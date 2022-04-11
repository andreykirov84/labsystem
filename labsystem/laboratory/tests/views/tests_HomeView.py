from django.test import TestCase
from django.urls import reverse

from labsystem.auth_app.models import LimsUser
from labsystem.laboratory.views.main_views import HomeView


class HomeViewTests(TestCase):
    TEMPLATE = 'main/home_page.html'
    USERNAME = 'John'
    PASSWORD = '1234'

    def setUp(self):
        pass

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_get__expect_correct_template(self):
        response = self.client.get(reverse('index'))
        self.assertTemplateUsed(response, self.TEMPLATE)

    # def test_get__expect_context_user_to_be(self):
    #     response = self.client.get('')
    #     expected = response.user
    #     actual = response.context[HomeView.context_user_key]
    #     self.assertEqual(expected, actual)

    # def test_pagination_is_ten(self):
    #     response = self.client.get(reverse('authors'))
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTrue('is_paginated' in response.context)
    #     self.assertTrue(response.context['is_paginated'] == True)
    #     self.assertEqual(len(response.context['author_list']), 10)

    # def test_user_create__when_all_valid__expect_to_create(self):
    #     user_data = {
    #         'username': '',
    #         'password': '',
    #     }
    #     self.client.post(
    #         reverse('url'),
    #         data=user_data,
    #     )
    #
    #     user = LimsUser.objects.first()
    #     # As we do integration tests it's OK to use many asserts
    #     self.assertIsNone(user)
    #     self.assertEqual(user_data['username'], user.username)
    #     self.assertEqual(user_data['password'], user.password)

    def test_unauthenticated_user_can_see_page(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_authenticated_patient_user_can_see_page(self):
        user = LimsUser.objects.create_patient_user(self.USERNAME, self.PASSWORD)
        self.client.force_login(user=user)
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_authenticated_staff_user_can_see_page(self):
        user = LimsUser.objects.create_staff_user(self.USERNAME, self.PASSWORD)
        self.client.force_login(user=user)
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_authenticated_physician_user_can_see_page(self):
        user = LimsUser.objects.create_physician_user(self.USERNAME, self.PASSWORD)
        self.client.force_login(user=user)
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)




