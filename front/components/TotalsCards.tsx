import { formatPen, type ReportTotals } from "@/lib/reports";

type Props = {
  totals: ReportTotals;
};

export default function TotalsCards({ totals }: Props) {
  return (
    <div className="grid gap-4 md:grid-cols-3">
      <article className="rounded-lg border p-4">
        <h2 className="text-sm text-gray-500">Cantidad de ventas</h2>
        <p className="mt-2 text-2xl font-semibold">{totals.sales_count}</p>
      </article>

      <article className="rounded-lg border p-4">
        <h2 className="text-sm text-gray-500">Ingresos</h2>
        <p className="mt-2 text-2xl font-semibold">
          {formatPen(totals.revenue_eur)}
        </p>
      </article>

      <article className="rounded-lg border p-4">
        <h2 className="text-sm text-gray-500">Ticket promedio</h2>
        <p className="mt-2 text-2xl font-semibold">
          {formatPen(totals.avg_ticket_eur)}
        </p>
      </article>
    </div>
  );
}