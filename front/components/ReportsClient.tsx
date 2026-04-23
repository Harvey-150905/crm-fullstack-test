"use client";

import { useEffect, useState } from "react";
import {
  getSalesReport,
  type ReportFilters,
  type ReportResponse,
} from "@/lib/reports";
import ShopSelector from "./ShopSelector";
import DateRangeInput from "./DateRangeInput";
import TotalsCards from "./TotalsCards";
import TopProductsTable from "./TopProductsTable";
import TotalsSkeleton from "./TotalsSkeleton";
import TableSkeleton from "./TableSkeleton";

type ShopOption = {
  id: number;
  name: string;
};

type Props = {
  initialData: ReportResponse;
  initialFilters: ReportFilters;
  shops: ShopOption[];
};

function toDateInputValue(isoString: string) {
  return isoString.slice(0, 10);
}

function toRangeIso(from: string, to: string) {
  return {
    from_date: `${from}T00:00:00`,
    to_date: `${to}T23:59:59`,
  };
}

function getErrorMessage(status?: number) {
  if (status === 422) return "Los filtros enviados no son validos.";
  if (status === 404) return "No se encontro el comercio solicitado.";
  if (status === 500) return "Ocurrió un error interno del servidor.";
  return "No se pudo cargar el reporte.";
}

export default function ReportsClient({
  initialData,
  initialFilters,
  shops,
}: Props) {
  const [shopId, setShopId] = useState(String(initialFilters.shop_id));
  const [dateRange, setDateRange] = useState({
    from: toDateInputValue(initialFilters.from_date),
    to: toDateInputValue(initialFilters.to_date),
  });

  const [data, setData] = useState<ReportResponse>(initialData);
  const [loadingTotals, setLoadingTotals] = useState(false);
  const [loadingTable, setLoadingTable] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");

  useEffect(() => {
    if (dateRange.from && dateRange.to && dateRange.from > dateRange.to) {
        setErrorMessage("desde donde tiene que ser menor que hasta donde.");
        return;
    }

    const initialRange = toRangeIso(
      toDateInputValue(initialFilters.from_date),
      toDateInputValue(initialFilters.to_date)
    );

    const isInitialRequest =
      String(initialFilters.shop_id) === String(shopId) &&
      initialRange.from_date === `${dateRange.from}T00:00:00` &&
      initialRange.to_date === `${dateRange.to}T23:59:59`;

    if (isInitialRequest) return;

    const range = toRangeIso(dateRange.from, dateRange.to);

    const requestFilters = {
      shop_id: shopId,
      from_date: range.from_date,
      to_date: range.to_date,
      page_size: 5,
    };

    let cancelled = false;

    async function loadReport() {
      setErrorMessage("");
      setLoadingTotals(true);
      setLoadingTable(true);

      try {
        const nextData = await getSalesReport(requestFilters);
        if (!cancelled) {
          setData(nextData);
        }
      } catch (err) {
        const status = (err as Error & { status?: number }).status;
        if (!cancelled) {
          setErrorMessage(getErrorMessage(status));
        }
      } finally {
        if (!cancelled) {
          setLoadingTotals(false);
          setLoadingTable(false);
        }
      }
    }

    loadReport();

    return () => {
      cancelled = true;
    };
  }, [shopId, dateRange.from, dateRange.to]);

  return (
    <section className="space-y-6">
      <div className="grid gap-4 md:grid-cols-3">
        <ShopSelector
          value={shopId}
          onChange={setShopId}
          options={shops}
        />

        <DateRangeInput value={dateRange} onChange={setDateRange} />
      </div>

      {errorMessage ? (
        <div
          className="rounded-lg border border-red-300 bg-red-50 p-4 text-red-700"
          role="alert"
        >
          {errorMessage}
        </div>
      ) : null}

      <section aria-busy={loadingTotals}>
        {loadingTotals ? (
          <TotalsSkeleton />
        ) : (
          <TotalsCards totals={data.totals} />
        )}
      </section>

      <section aria-busy={loadingTable}>
        {loadingTable ? (
          <TableSkeleton />
        ) : (
          <TopProductsTable products={data.top_products} />
        )}
      </section>
    </section>
  );
}