from django.db.models import Sum, Count, F, IntegerField, ExpressionWrapper
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
from django.utils.dateparse import parse_datetime
import pytz

from .models import Shop, Sale, SaleItem


@api_view(['GET'])
def sales_report(request):
    shop_id = request.GET.get('shop_id')
    from_date = request.GET.get('from_date')
    to_date = request.GET.get('to_date')
    page_size = request.GET.get('page_size', 5)

    if not shop_id or not from_date or not to_date:
        return Response(
            {"error": "missing_params"},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        shop = Shop.objects.get(id=shop_id)
        tz = pytz.timezone(shop.tz)

        from_dt = parse_datetime(from_date)
        to_dt = parse_datetime(to_date)

        if from_dt is None or to_dt is None:
            return Response(
                {"error": "invalid_date_format"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # si NO tiene timezone → asignar la del shop
        if from_dt.tzinfo is None:
            from_dt = tz.localize(from_dt)

        if to_dt.tzinfo is None:
            to_dt = tz.localize(to_dt)

        # convertir a UTC
        from_dt_utc = from_dt.astimezone(pytz.UTC)
        to_dt_utc = to_dt.astimezone(pytz.UTC)

    except Shop.DoesNotExist:
        return Response(
            {"error": "shop_not_found"},
            status=status.HTTP_404_NOT_FOUND
        )

    page_size = int(page_size)
    page_size = min(page_size, 50)

    sales = Sale.objects.filter(
        shop=shop,
        refunded=False,
        created_at__gte=from_dt_utc,
        created_at__lte=to_dt_utc
    )

    totals = sales.aggregate(
        total_cents=Sum('total_cents'),
        sales_count=Count('id')
    )

    total_cents = totals['total_cents'] or 0
    sales_count = totals['sales_count'] or 0
    avg_ticket_eur = total_cents / sales_count if sales_count > 0 else 0

    revenue_eur = round(total_cents / 100, 2)
    avg_ticket_eur = round(avg_ticket_eur / 100, 2)

    top_products = (
        SaleItem.objects
        .filter(sale__in=sales)
        .annotate(
            line_revenue_eur=ExpressionWrapper(
                F('qty') * F('unit_price_cents'),
                output_field=IntegerField()
            )
        )
        .values('product__sku', 'product__name')
        .annotate(
            qty=Sum('qty'),
            revenue_eur=Sum('line_revenue_eur')
        )
        .order_by('-revenue_eur')[:page_size]
    )

    return Response({
        "shop": {
            "id": shop.id,
            "name": shop.name
        },
        "period": {
            "from": from_date,
            "to": to_date,
            "tz": shop.tz
        },
        "totals": {
            "sales_count": sales_count,
            "revenue_eur": revenue_eur,
            "avg_ticket_eur": avg_ticket_eur
        },
        "top_products": [
            {
                "sku": p["product__sku"],
                "name": p["product__name"],
                "qty": p["qty"],
                "revenue_eur": round((p["revenue_eur"] or 0) / 100, 2)
            }
            for p in top_products
        ]
    })