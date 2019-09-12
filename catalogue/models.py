from django.db import models


class Category(models.Model):
    """ カテゴリー
    """
    name = models.CharField("カテゴリー名", max_length=32)


class Product(models.Model):
    """ 製品
    """
    category = models.ForeignKey(Category, null=True, blank=True,
                                 on_delete=models.SET_NULL)
    name = models.CharField("商品名", max_length=128)
    price = models.PositiveIntegerField("価格")
