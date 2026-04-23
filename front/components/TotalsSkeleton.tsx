export default function TotalsSkeleton() {
  return (
    <div className="grid gap-4 md:grid-cols-3">
      {Array.from({ length: 3 }).map((_, idx) => (
        <div
          key={idx}
          className="animate-pulse rounded-lg border p-4"
        >
          <div className="mb-3 h-4 w-24 rounded bg-gray-200" />
          <div className="h-8 w-32 rounded bg-gray-200" />
        </div>
      ))}
    </div>
  );
}