import { formatPen, type TopProduct } from "@/lib/reports";

type Props = {
  products: TopProduct[];
};

export default function TopProductsTable({ products }: Props) {
  return (
    <div className="overflow-x-auto rounded-lg border">
      <table className="min-w-full border-collapse">
        <caption className="p-4 text-left text-sm font-medium">
          Tabla de productos más vendidos por facturación
        </caption>

        <thead>
          <tr className="bg-gray-100">
            <th scope="col" className="border-b p-3 text-left">
              SKU
            </th>
            <th scope="col" className="border-b p-3 text-left">
              Producto
            </th>
            <th scope="col" className="border-b p-3 text-left">
              Cantidad
            </th>
            <th scope="col" className="border-b p-3 text-left">
              Facturación
            </th>
          </tr>
        </thead>

        <tbody>
          {products.length === 0 ? (
            <tr>
              <td colSpan={4} className="p-4 text-center text-gray-500">
                No hay productos para mostrar.
              </td>
            </tr>
          ) : (
            products.map((product) => (
              <tr key={product.sku}>
                <td className="border-b p-3">{product.sku}</td>
                <td className="border-b p-3">{product.name}</td>
                <td className="border-b p-3">{product.qty}</td>
                <td className="border-b p-3">
                  {formatPen(product.revenue_eur)}
                </td>
              </tr>
            ))
          )}
        </tbody>
      </table>
    </div>
  );
}