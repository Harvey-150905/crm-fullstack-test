"use client";

type Value = {
  from: string;
  to: string;
};

type Props = {
  value: Value;
  onChange: (value: Value) => void;
};

export default function DateRangeInput({ value, onChange }: Props) {

  const fmt = (d: string) => {
    if (!d) return "—";

    const [year, month, day] = d.split("-");
    return `${day}/${month}/${year}`;
  };

  return (
    <div className="flex flex-col gap-2">
      <span className="text-sm font-medium">Rango de fechas</span>

      <div className="grid gap-2 md:grid-cols-2">
        <input
          type="date"
          value={value.from || ""}
          onChange={(e) => onChange({ ...value, from: e.target.value })}
          className="rounded-md border p-2"
          aria-label="Fecha desde"
        />

        <input
          type="date"
          value={value.to || ""}
          onChange={(e) => onChange({ ...value, to: e.target.value })}
          className="rounded-md border p-2"
          aria-label="Fecha hasta"
        />
      </div>

      <span className="text-sm text-gray-600">
        {fmt(value.from)} — {fmt(value.to)}
      </span>
    </div>
  );
}