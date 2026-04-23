import ReportsClient from "@/components/ReportsClient";
import { getSalesReport } from "@/lib/reports";

export default async function ReportsPage() {
  const initialFilters = {
    shop_id: 1,
    from_date: "2025-01-01T00:00:00",
    to_date: "2025-12-31T23:59:59",
    page_size: 5,
  };

  const initialData = await getSalesReport(initialFilters);

  const shops = [
    { id: 1, name: initialData.shop.name || "Shop 1" },
  ];

  return (
    <main className="mx-auto max-w-6xl p-6">
      <h1 className="mb-6 text-3xl font-bold">Reportes de ventas</h1>

      <ReportsClient
        initialData={initialData}
        initialFilters={initialFilters}
        shops={shops}
      />
    </main>
  );
}