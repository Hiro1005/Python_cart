from django.test import TestCase
from django.urls import reverse

from catalogue.models import Product


class TestCartList(TestCase):
    def test_get(self):
        Product.objects.create(id=1, name="テスト1", price=100)
        Product.objects.create(id=2, name="テスト2", price=200)
        session = self.client.session
        session['cart'] = [1, 2]
        session.save()

        res = self.client.get(reverse('cart_list'))
        self.assertTemplateUsed(res, 'cart/list.html')
        self.assertContains(res, 'テスト1: 100円')
        self.assertContains(res, 'テスト2: 200円')
        self.assertContains(res, '合計金額: 300円')

    def test_get_product_not_exist(self):
        session = self.client.session
        session['cart'] = [1]
        session.save()
        res = self.client.get(reverse('cart_list'))
        self.assertContains(res, '合計金額: 0円')

    def test_get_cart_empty(self):
        res = self.client.get(reverse('cart_list'))
        self.assertContains(res, '合計金額: 0円')


class TestCartAdd(TestCase):
    def test_post_empty_cart(self):
        Product.objects.create(id=1, name='テスト1', price=100)
        res = self.client.post(reverse('cart_add', args=(1,)))
        self.assertRedirects(res, reverse('product_list'))
        self.assertEqual(self.client.session['cart'], [1])

    def test_post_cart_existed(self):
        Product.objects.create(id=1, name='テスト1', price=100)
        Product.objects.create(id=2, name='テスト2', price=200)
        session = self.client.session
        session['cart'] = [1]
        session.save()

        res = self.client.post(reverse('cart_add', args=(2,)))
        self.assertRedirects(res, reverse('product_list'))
        self.assertEqual(self.client.session['cart'], [1, 2])

    def test_404(self):
        res = self.client.post(reverse('cart_add', args=(1,)))
        self.assertEqual(res.status_code, 404)

    def test_405(self):
        res = self.client.get(reverse('cart_add', args=(1,)))
        self.assertEqual(res.status_code, 405)


class TestCartDelete(TestCase):
    def test_post_empty_cart(self):
        res = self.client.post(reverse('cart_delete', args=(1,)))
        self.assertRedirects(res, reverse('cart_list'))
        self.assertNotIn('cart', self.client.session)

    def test_post_cart_existed(self):
        session = self.client.session
        session['cart'] = [1, 2]
        session.save()

        res = self.client.post(reverse('cart_delete', args=(1,)))
        self.assertRedirects(res, reverse('cart_list'))
        self.assertEqual(self.client.session['cart'], [2])

    def test_405(self):
        res = self.client.get(reverse('cart_delete', args=(1,)))
        self.assertEqual(res.status_code, 405)
        