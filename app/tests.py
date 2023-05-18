from django.test import TestCase, RequestFactory
from django.urls import reverse
from .views import Crud



class MyViewTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_my_view(self):
        url = reverse('get_or_post')  
        request = self.factory.get(url)
        response = Crud.as_view()(request)

        self.assertEqual(response.status_code, 401)