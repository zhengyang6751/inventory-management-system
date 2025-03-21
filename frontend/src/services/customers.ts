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

export const getCustomers = async (): Promise<Customer[]> => {
  const response = await api.get("/customers");
  return response.data;
};

export const createCustomer = async (
  data: CustomerCreate
): Promise<Customer> => {
  const response = await api.post("/customers", data);
  return response.data;
};
