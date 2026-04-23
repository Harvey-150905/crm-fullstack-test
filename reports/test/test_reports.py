import pytest
import datetime
import pytz
from rest_framework.test import APIClient
from django.utils import timezone
from reports.models import Shop, Sale, SaleItem, Product


@pytest.mark.django_db
def test_sales_report_normal():
    client = APIClient()

    shop = Shop.objects.create(name="Test Shop", tz="America/Lima")
    product = Product.objects.create(sku="A1", name="Coca", price_cents=100)

    fixed_dt = datetime.datetime(2025, 1, 15, 12, 0, tzinfo=pytz.UTC)

    sale = Sale.objects.create(
        shop=shop,
        created_at=fixed_dt,
        total_cents=200,
        refunded=False
    )

    SaleItem.objects.create(
        sale=sale,
        product=product,
        qty=2,
        unit_price_cents=100
    )

    response = client.get("/api/reports/sales/", {
        "shop_id": shop.id,
        "from_date": "2025-01-01T00:00:00",
        "to_date": "2025-12-31T23:59:59"
    })

    assert response.status_code == 200
    data = response.json()

    assert data["totals"]["sales_count"] == 1
    assert data["totals"]["revenue_eur"] == 2.0


@pytest.mark.django_db
def test_sales_report_no_sales():
    client = APIClient()

    shop = Shop.objects.create(name="Empty Shop", tz="America/Lima")

    response = client.get("/api/reports/sales/", {
        "shop_id": shop.id,
        "from_date": "2025-01-01T00:00:00",
        "to_date": "2025-12-31T23:59:59"
    })

    data = response.json()

    assert data["totals"]["sales_count"] == 0
    assert data["totals"]["revenue_eur"] == 0.0
    assert data["totals"]["avg_ticket_eur"] == 0.0


@pytest.mark.django_db
def test_sales_report_excludes_refunds():
    client = APIClient()

    shop = Shop.objects.create(name="Shop", tz="America/Lima")

    fixed_dt = datetime.datetime(2025, 1, 15, 12, 0, tzinfo=pytz.UTC)

    Sale.objects.create(
        shop=shop,
        created_at=fixed_dt,
        total_cents=1000,
        refunded=True
    )

    response = client.get("/api/reports/sales/", {
        "shop_id": shop.id,
        "from_date": "2025-01-01T00:00:00",
        "to_date": "2025-12-31T23:59:59"
    })

    data = response.json()

    assert data["totals"]["sales_count"] == 0


@pytest.mark.django_db
def test_sales_report_timezone():
    client = APIClient()

    shop = Shop.objects.create(name="TZ Shop", tz="America/Lima")

    # 23:30 UTC → en Lima sigue siendo mismo día
    dt = datetime.datetime(2025, 1, 1, 23, 30, tzinfo=pytz.UTC)

    Sale.objects.create(
        shop=shop,
        created_at=dt,
        total_cents=1000,
        refunded=False
    )

    response = client.get("/api/reports/sales/", {
        "shop_id": shop.id,
        "from_date": "2025-01-01T00:00:00",
        "to_date": "2025-01-01T23:59:59"
    })

    data = response.json()

    assert data["totals"]["sales_count"] == 1


@pytest.mark.django_db
def test_top_products_order():
    client = APIClient()

    shop = Shop.objects.create(name="Shop", tz="America/Lima")
    p1 = Product.objects.create(sku="A1", name="A", price_cents=100)
    p2 = Product.objects.create(sku="B1", name="B", price_cents=100)

    fixed_dt = datetime.datetime(2025, 1, 15, 12, 0, tzinfo=pytz.UTC)

    sale = Sale.objects.create(
        shop=shop,
        created_at=fixed_dt,
        total_cents=300,
        refunded=False
    )

    SaleItem.objects.create(sale=sale, product=p1, qty=2, unit_price_cents=100)
    SaleItem.objects.create(sale=sale, product=p2, qty=1, unit_price_cents=100)

    response = client.get("/api/reports/sales/", {
        "shop_id": shop.id,
        "from_date": "2025-01-01T00:00:00",
        "to_date": "2025-12-31T23:59:59"
    })

    data = response.json()

    assert len(data["top_products"]) == 2
    assert data["top_products"][0]["sku"] == "A1"