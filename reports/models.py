from django.db import models

# Create your models here.
class Shop(models.Model):
    name = models.CharField(max_length=120)
    tz = models.CharField(max_length=64, default='America/Lima')

class Product(models.Model):
    sku = models.CharField(max_length=32, unique=True)
    name = models.CharField(max_length=200)
    price_cents = models.IntegerField()

class Sale(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    created_at = models.DateTimeField()
    total_cents = models.IntegerField()
    refunded = models.BooleanField(default=False)

class SaleItem(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    qty = models.IntegerField()
    unit_price_cents = models.IntegerField()