import React, { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { useToast } from "@/components/ui/use-toast";
import SaleModal from "@/components/SaleModal";
import {
  getSales,
  createSale,
  type Sale,
  type CreateSaleDTO,
} from "@/services/sales";
import { getProducts, type Product } from "@/services/products";
import { getCustomers, type Customer } from "@/services/customers";

export default function Sales() {
  const [sales, setSales] = useState<Sale[]>([]);
  const [products, setProducts] = useState<Product[]>([]);
  const [customers, setCustomers] = useState<Customer[]>([]);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const { toast } = useToast();

  useEffect(() => {
    fetchSales();
    fetchProducts();
    fetchCustomers();
  }, []);

  const fetchSales = async () => {
    try {
      const data = await getSales();
      setSales(data);
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to fetch sales",
        variant: "destructive",
      });
    }
  };

  const fetchProducts = async () => {
    try {
      const data = await getProducts();
      setProducts(data);
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to fetch products",
        variant: "destructive",
      });
    }
  };

  const fetchCustomers = async () => {
    try {
      const data = await getCustomers();
      setCustomers(data);
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to fetch customers",
        variant: "destructive",
      });
    }
  };

  const handleCreateSale = async (data: CreateSaleDTO) => {
    try {
      await createSale(data);
      setIsModalOpen(false);
      fetchSales();
      toast({
        title: "Success",
        description: "Sale created successfully",
      });
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to create sale",
        variant: "destructive",
      });
    }
  };

  return (
    <div className="container mx-auto py-6">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold">Sales</h1>
        <Button onClick={() => setIsModalOpen(true)}>Add Sale</Button>
      </div>

      <div className="bg-white rounded-lg shadow">
        <table className="min-w-full">
          <thead>
            <tr className="border-b">
              <th className="px-6 py-3 text-left">Product</th>
              <th className="px-6 py-3 text-left">Customer</th>
              <th className="px-6 py-3 text-left">Quantity</th>
              <th className="px-6 py-3 text-left">Unit Price</th>
              <th className="px-6 py-3 text-left">Total Amount</th>
              <th className="px-6 py-3 text-left">Date</th>
            </tr>
          </thead>
          <tbody>
            {sales.map((sale) => (
              <tr key={sale.id} className="border-b">
                <td className="px-6 py-4">{sale.product.name}</td>
                <td className="px-6 py-4">{sale.customer.full_name}</td>
                <td className="px-6 py-4">{sale.quantity}</td>
                <td className="px-6 py-4">${sale.unit_price.toFixed(2)}</td>
                <td className="px-6 py-4">${sale.total_amount.toFixed(2)}</td>
                <td className="px-6 py-4">
                  {new Date(sale.created_at).toLocaleDateString()}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <SaleModal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        onSubmit={handleCreateSale}
        products={products}
        customers={customers}
        onCustomerCreated={fetchCustomers}
      />
    </div>
  );
}
