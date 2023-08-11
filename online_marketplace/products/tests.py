from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from online_marketplace.products.models import Product, Category
from online_marketplace.products.forms import ProductUpdateForm


UserModel = get_user_model()


class ProductTests(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user(username='testuser', password='testpass')
        self.category = Category.objects.create(name='Electronics')
        self.product = Product.objects.create(name='Test Product', description='This is a test product',  price=100,
                                              user=self.user,
                                              category=self.category)

    def test_create_product(self):
        self.assertEqual(Product.objects.count(), 1)

    def test_product_update_form_invalid(self):
        form_data = {'name': '', 'description': 'This is an updated product'}
        form = ProductUpdateForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_product_list_view(self):
        url = reverse('product list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_product_detail_view(self):
        url = reverse('product details', kwargs={'pk': self.product.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_product_create_view_authenticated(self):
        self.client.login(username='testuser', password='testpass')
        url = reverse('product create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_product_update_view_authenticated(self):
        self.client.login(username='testuser', password='testpass')
        url = reverse('product update', kwargs={'pk': self.product.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_product_delete_view_authenticated(self):
        self.client.login(username='testuser', password='testpass')
        url = reverse('product delete', kwargs={'pk': self.product.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
