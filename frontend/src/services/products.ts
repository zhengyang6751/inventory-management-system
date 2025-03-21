import { api } from "@/lib/axios";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

export interface Product {
  id: number;
  name: string;
  description: string;
  sku: string;
  barcode: string;
  price: number;
  cost: number;
  stock: number;
  min_quantity: number;
  category_id: number;
  supplier_id: number;
  created_at: string;
  updated_at: string;
  category?: Category;
  supplier?: Supplier;
}

export interface Category {
  id: number;
  name: string;
  description: string | null;
}

export interface Supplier {
  id: number;
  name: string;
  contact_name: string | null;
  email: string | null;
  phone: string | null;
  address: string | null;
}

export interface CreateProductDTO {
  name: string;
  description: string;
  sku: string;
  barcode: string;
  price: number;
  cost: number;
  stock: number;
  min_quantity: number;
  category_id: number;
  supplier_id: number;
}

export const getProducts = async (): Promise<Product[]> => {
  const response = await api.get("/products");
  return response.data;
};

export async function getProduct(id: number) {
  const response = await api.get<Product>(`/products/${id}`);
  return response.data;
}

export const createProduct = async (
  data: CreateProductDTO
): Promise<Product> => {
  const response = await api.post("/products", data);
  return response.data;
};

export const updateProduct = async (
  id: number,
  data: Partial<CreateProductDTO>
): Promise<Product> => {
  const response = await api.put(`/products/${id}`, data);
  return response.data;
};

export const deleteProduct = async (id: number): Promise<void> => {
  await api.delete(`/products/${id}`);
};
