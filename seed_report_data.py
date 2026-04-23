from reports.models import Shop, Product, Sale, SaleItem
from datetime import datetime, timedelta
import pytz

# limpiar si quieres empezar de cero
SaleItem.objects.all().delete()
Sale.objects.all().delete()
Product.objects.all().delete()
Shop.objects.all().delete()

shop = Shop.objects.create(
    id=1,
    name="Central",
    tz="America/Lima",
)

p1 = Product.objects.create(
    sku="AB-01",
    name="Producto A",
    price_cents=1000,
)

p2 = Product.objects.create(
    sku="CD-02",
    name="Producto B",
    price_cents=2000,
)

tz = pytz.timezone("America/Lima")

for i in range(10):
    dt_local = tz.localize(datetime(2025, 1, 10, 12, 0) + timedelta(days=i))

    sale = Sale.objects.create(
        shop=shop,
        created_at=dt_local.astimezone(pytz.UTC),
        total_cents=3000,
        refunded=False,
    )

    SaleItem.objects.create(
        sale=sale,
        product=p1,
        qty=2,
        unit_price_cents=1000,
    )

    SaleItem.objects.create(
        sale=sale,
        product=p2,
        qty=1,
        unit_price_cents=1000,
    )

print("LISTO")