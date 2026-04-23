"use client";

import React from "react";

type ShopOption = {
  id: number;
  name: string;
};

type Props = {
  value: string;
  onChange: (value: string) => void;
  options: ShopOption[];
};

function ShopSelectorComponent({ value, onChange, options }: Props) {
  return (
    <div className="flex flex-col gap-2">
      <label htmlFor="shop" className="text-sm font-medium">
        Comercio
      </label>

      <select
        id="shop"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        className="rounded-md border p-2"
      >
        {options.map((shop) => (
          <option key={shop.id} value={shop.id}>
            {shop.name}
          </option>
        ))}
      </select>
    </div>
  );
}

const ShopSelector = React.memo(ShopSelectorComponent);

export default ShopSelector;