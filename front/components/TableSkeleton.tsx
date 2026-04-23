export default function TableSkeleton() {
  return (
    <div className="rounded-lg border p-4">
      <div className="animate-pulse space-y-3">
        <div className="h-4 w-48 rounded bg-gray-200" />
        <div className="h-10 w-full rounded bg-gray-200" />
        <div className="h-10 w-full rounded bg-gray-200" />
        <div className="h-10 w-full rounded bg-gray-200" />
      </div>
    </div>
  );
}