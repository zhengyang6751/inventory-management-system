import { api } from "@/lib/axios";

export interface Customer {
  id: number;
  full_name: string;
  email: string | null;
  phone: string | null;
  address: string | null;
  created_at: string;
  updated_at: string | null;
}

export interface CustomerCreate {
  full_name: string;
  email?: string;
  phone?: string;
  address?: string;
}

export interface Sale {
  id: number;
  product_id: number;
  customer_id: number;
  quantity: number;
  unit_price: number;
  total_amount: number;
  notes?: string;
  created_at: string;
  product: {
    id: number;
    name: string;
    price: number;
    stock: number;
  };
  customer: {
    id: number;
    full_name: string;
    email: string;
  };
}

export interface CreateSaleDTO {
  product_id: number;
  customer_id: number;
  quantity: number;
  unit_price: number;
  notes?: string;
}

export interface Return {
  id: number;
  sale_id: number;
  product_id: number;
  quantity: number;
  reason: string | null;
  notes: string | null;
  created_by: number;
  created_at: string;
}

export interface ReturnCreate {
  sale_id: number;
  product_id: number;
  quantity: number;
  reason?: string;
  notes?: string;
}

export interface SalesSummary {
  total_sales: number;
  total_revenue: number;
}

// Customer API functions
export async function getCustomers() {
  const response = await api.get<Customer[]>("/customers");
  return response.data;
}

export async function createCustomer(customer: CustomerCreate) {
  const response = await api.post<Customer>("/customers", customer);
  return response.data;
}

// Sales API functions
export const getSales = async (): Promise<Sale[]> => {
  const response = await api.get("/sales");
  return response.data;
};

export const createSale = async (data: CreateSaleDTO): Promise<Sale> => {
  const response = await api.post("/sales", data);
  return response.data;
};

export async function getSalesSummary(start_date: string, end_date: string) {
  const response = await api.get<SalesSummary>("/sales/summary", {
    params: { start_date, end_date },
  });
  return response.data;
}

// Returns API functions
export async function getReturns(params?: {
  sale_id?: number;
  product_id?: number;
}) {
  const response = await api.get<Return[]>("/sales/returns", {
    params,
  });
  return response.data;
}

export async function createReturn(return_: ReturnCreate) {
  const response = await api.post<Return>("/sales/returns", return_);
  return response.data;
}
