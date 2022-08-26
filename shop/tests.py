from django.urls import reverse_lazy
from rest_framework.test import APITestCase

from shop.models import Category


class TestCategory(APITestCase):
    # We store the endpoint url in a class attribute to be able to use it more easily in
    # each of our tests
    url = reverse_lazy('category-list')

    def format_datetime(self, value):
        # This method is a helper allowing to format a date in character string in the same format as
        # that of the API
        return value.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

    def test_list(self):
        # Let's create two categories of which only one is active
        category = Category.objects.create(name='Fruits', active=True)
        Category.objects.create(name='Légumes', active=False)

        # We make the call in GET using the client of the test class
        response = self.client.get(self.url)
        # We check that the status code is 200
        # and the returned values are the expected ones
        self.assertEqual(response.status_code, 200)
        excepted = [
            {
                'id': category.pk,
                'name': category.name,
                'date_created': self.format_datetime(category.date_created),
                'date_updated': self.format_datetime(category.date_updated),
            }
        ]
        self.assertEqual(excepted, response.json())

    def test_create(self):
        # We check that no category exists before attempting to create one
        self.assertFalse(Category.objects.exists())
        response = self.client.post(self.url, data={'name': 'New category'})
        # Let's check that the status code is in error and prevents us from creating a category
        self.assertEqual(response.status_code, 405)
        # Finally, let's check that no new category has been created despite the status code 405
        self.assertFalse(Category.objects.exists())
