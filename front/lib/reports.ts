export type ReportTotals = {
  sales_count: number;
  revenue_eur: number;
  avg_ticket_eur: number;
};

export type TopProduct = {
  sku: string;
  name: string;
  qty: number;
  revenue_eur: number;
};

export type ReportResponse = {
  shop: {
    id: number;
    name: string;
  };
  period: {
    from: string;
    to: string;
    tz: string;
  };
  totals: ReportTotals;
  top_products: TopProduct[];
};

export type ReportFilters = {
  shop_id: number | string;
  from_date: string;
  to_date: string;
  page_size?: number | string;
};

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000";

function buildUrl(filters: ReportFilters) {
  const params = new URLSearchParams({
    shop_id: String(filters.shop_id),
    from_date: filters.from_date,
    to_date: filters.to_date,
    page_size: String(filters.page_size ?? 5),
  });

  return `${API_BASE}/api/reports/sales/?${params.toString()}`;
}

export async function getSalesReport(
  filters: ReportFilters,
  options?: RequestInit
): Promise<ReportResponse> {
  const res = await fetch(buildUrl(filters), {
    method: "GET",
    cache: "no-store",
    ...options,
  });

  if (!res.ok) {
    const error = new Error("Request failed") as Error & { status?: number };
    error.status = res.status;
    throw error;
  }

  return res.json();
}

export function formatPen(value: number) {
  return new Intl.NumberFormat("es-PE", {
    style: "currency",
    currency: "PEN",
  }).format(value);
}