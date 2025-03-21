import React, { useState } from "react";
import { Dialog } from "@headlessui/react";
import { useForm } from "react-hook-form";
import { Button } from "@/components/ui/button";
import { type Product } from "@/services/products";
import { type Customer, type CustomerCreate } from "@/services/customers";
import { type CreateSaleDTO } from "@/services/sales";
import { createCustomer } from "@/services/customers";
import { useToast } from "@/components/ui/use-toast";

interface SaleModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSubmit: (data: CreateSaleDTO) => void;
  products: Product[];
  customers: Customer[];
  onCustomerCreated?: () => void;
}

export default function SaleModal({
  isOpen,
  onClose,
  onSubmit,
  products,
  customers,
  onCustomerCreated,
}: SaleModalProps) {
  const { toast } = useToast();
  const [customerSearch, setCustomerSearch] = useState("");
  const [showCustomerSuggestions, setShowCustomerSuggestions] = useState(false);
  const [selectedCustomer, setSelectedCustomer] = useState<Customer | null>(
    null
  );
  const [showNewCustomerForm, setShowNewCustomerForm] = useState(false);

  const {
    register,
    handleSubmit,
    watch,
    setValue,
    formState: { errors },
    reset,
  } = useForm<CreateSaleDTO>();

  const {
    register: registerCustomer,
    handleSubmit: handleSubmitCustomer,
    formState: { errors: customerErrors },
    reset: resetCustomer,
  } = useForm<CustomerCreate>();

  const selectedProductId = watch("product_id");
  const selectedProduct = products.find(
    (p) => p.id === Number(selectedProductId)
  );

  React.useEffect(() => {
    if (selectedProduct) {
      setValue("unit_price", selectedProduct.price);
    }
  }, [selectedProduct, setValue]);

  React.useEffect(() => {
    if (!isOpen) {
      reset();
      setCustomerSearch("");
      setSelectedCustomer(null);
      setShowNewCustomerForm(false);
    }
  }, [isOpen, reset]);

  const filteredCustomers = customers.filter(
    (customer) =>
      customer.full_name.toLowerCase().includes(customerSearch.toLowerCase()) ||
      (customer.email &&
        customer.email.toLowerCase().includes(customerSearch.toLowerCase()))
  );

  const handleCustomerSelect = (customer: Customer) => {
    setSelectedCustomer(customer);
    setCustomerSearch(customer.full_name);
    setValue("customer_id", customer.id);
    setShowCustomerSuggestions(false);
  };

  const handleCreateCustomer = async (data: CustomerCreate) => {
    try {
      const newCustomer = await createCustomer(data);
      setSelectedCustomer(newCustomer);
      setValue("customer_id", newCustomer.id);
      setShowNewCustomerForm(false);
      resetCustomer();
      if (onCustomerCreated) {
        onCustomerCreated();
      }
      toast({
        title: "Success",
        description: "Customer created successfully",
      });
    } catch (error: any) {
      if (
        error.response?.status === 400 &&
        error.response?.data?.detail?.includes("email already exists")
      ) {
        toast({
          title: "Customer Already Exists",
          description:
            "A customer with this email already exists. Please search for them using their name or email.",
          variant: "destructive",
        });
        setCustomerSearch(data.email || "");
        setShowNewCustomerForm(false);
        setShowCustomerSuggestions(true);
      } else {
        toast({
          title: "Error",
          description: "Failed to create customer. Please try again.",
          variant: "destructive",
        });
      }
    }
  };

  const onSubmitForm = (data: CreateSaleDTO) => {
    if (!selectedCustomer) {
      toast({
        title: "Error",
        description: "Please select a customer",
        variant: "destructive",
      });
      return;
    }
    onSubmit({
      ...data,
      product_id: Number(data.product_id),
      customer_id: selectedCustomer.id,
      unit_price: Number(data.unit_price),
      quantity: Number(data.quantity),
    });
  };

  return (
    <Dialog
      open={isOpen}
      onClose={onClose}
      className="fixed inset-0 z-10 overflow-y-auto"
    >
      <div className="flex min-h-screen items-center justify-center">
        <Dialog.Overlay className="fixed inset-0 bg-black opacity-30" />

        <div className="relative mx-auto w-full max-w-md rounded-lg bg-white p-6">
          <Dialog.Title className="mb-4 text-lg font-medium">
            New Sale
          </Dialog.Title>

          <form onSubmit={handleSubmit(onSubmitForm)} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700">
                Product
              </label>
              <select
                {...register("product_id", { required: "Product is required" })}
                className="mt-1 block w-full rounded-md border border-gray-300 py-2 px-3 shadow-sm focus:border-indigo-500 focus:outline-none focus:ring-indigo-500"
              >
                <option value="">Select a product</option>
                {products.map((product) => (
                  <option key={product.id} value={product.id}>
                    {product.name} - ${product.price} (Stock: {product.stock})
                  </option>
                ))}
              </select>
              {errors.product_id && (
                <p className="mt-1 text-sm text-red-600">
                  {errors.product_id.message}
                </p>
              )}
            </div>

            <div className="relative">
              <label className="block text-sm font-medium text-gray-700">
                Customer
              </label>
              <div className="flex gap-2">
                <input
                  type="text"
                  value={customerSearch}
                  onChange={(e) => {
                    setCustomerSearch(e.target.value);
                    setShowCustomerSuggestions(true);
                  }}
                  onFocus={() => setShowCustomerSuggestions(true)}
                  placeholder="Search customer..."
                  className="mt-1 block w-full rounded-md border border-gray-300 py-2 px-3 shadow-sm focus:border-indigo-500 focus:outline-none focus:ring-indigo-500"
                />
                <Button
                  type="button"
                  onClick={() => setShowNewCustomerForm(true)}
                  className="mt-1"
                >
                  New
                </Button>
              </div>
              {showCustomerSuggestions && customerSearch && (
                <div className="absolute z-10 mt-1 w-full rounded-md border border-gray-300 bg-white shadow-lg">
                  {filteredCustomers.length > 0 ? (
                    filteredCustomers.map((customer) => (
                      <div
                        key={customer.id}
                        onClick={() => handleCustomerSelect(customer)}
                        className="cursor-pointer px-4 py-2 hover:bg-gray-100"
                      >
                        <div>{customer.full_name}</div>
                        {customer.email && (
                          <div className="text-sm text-gray-500">
                            {customer.email}
                          </div>
                        )}
                      </div>
                    ))
                  ) : (
                    <div className="px-4 py-2 text-gray-500">
                      No customers found
                    </div>
                  )}
                </div>
              )}
            </div>

            {showNewCustomerForm && (
              <div className="space-y-4 rounded-md border border-gray-300 p-4">
                <h3 className="text-lg font-medium">New Customer</h3>
                <div>
                  <label className="block text-sm font-medium text-gray-700">
                    Full Name
                  </label>
                  <input
                    type="text"
                    {...registerCustomer("full_name", {
                      required: "Full name is required",
                    })}
                    className="mt-1 block w-full rounded-md border border-gray-300 py-2 px-3 shadow-sm focus:border-indigo-500 focus:outline-none focus:ring-indigo-500"
                  />
                  {customerErrors.full_name && (
                    <p className="mt-1 text-sm text-red-600">
                      {customerErrors.full_name.message}
                    </p>
                  )}
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700">
                    Email
                  </label>
                  <input
                    type="email"
                    {...registerCustomer("email", {
                      pattern: {
                        value: /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i,
                        message: "Invalid email address",
                      },
                    })}
                    className="mt-1 block w-full rounded-md border border-gray-300 py-2 px-3 shadow-sm focus:border-indigo-500 focus:outline-none focus:ring-indigo-500"
                  />
                  {customerErrors.email && (
                    <p className="mt-1 text-sm text-red-600">
                      {customerErrors.email.message}
                    </p>
                  )}
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700">
                    Phone
                  </label>
                  <input
                    type="tel"
                    {...registerCustomer("phone")}
                    className="mt-1 block w-full rounded-md border border-gray-300 py-2 px-3 shadow-sm focus:border-indigo-500 focus:outline-none focus:ring-indigo-500"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700">
                    Address
                  </label>
                  <input
                    type="text"
                    {...registerCustomer("address")}
                    className="mt-1 block w-full rounded-md border border-gray-300 py-2 px-3 shadow-sm focus:border-indigo-500 focus:outline-none focus:ring-indigo-500"
                  />
                </div>
                <div className="flex justify-end space-x-2">
                  <Button
                    type="button"
                    variant="outline"
                    onClick={() => setShowNewCustomerForm(false)}
                  >
                    Cancel
                  </Button>
                  <Button
                    type="button"
                    onClick={handleSubmitCustomer(handleCreateCustomer)}
                  >
                    Create Customer
                  </Button>
                </div>
              </div>
            )}

            <div>
              <label className="block text-sm font-medium text-gray-700">
                Quantity
              </label>
              <input
                type="number"
                {...register("quantity", {
                  required: "Quantity is required",
                  min: {
                    value: 1,
                    message: "Quantity must be at least 1",
                  },
                  max: {
                    value: selectedProduct?.stock || 0,
                    message: `Maximum quantity is ${
                      selectedProduct?.stock || 0
                    }`,
                  },
                })}
                className="mt-1 block w-full rounded-md border border-gray-300 py-2 px-3 shadow-sm focus:border-indigo-500 focus:outline-none focus:ring-indigo-500"
              />
              {errors.quantity && (
                <p className="mt-1 text-sm text-red-600">
                  {errors.quantity.message}
                </p>
              )}
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700">
                Unit Price
              </label>
              <input
                type="number"
                step="0.01"
                {...register("unit_price", {
                  required: "Unit price is required",
                  min: {
                    value: 0.01,
                    message: "Unit price must be greater than 0",
                  },
                })}
                className="mt-1 block w-full rounded-md border border-gray-300 py-2 px-3 shadow-sm focus:border-indigo-500 focus:outline-none focus:ring-indigo-500"
              />
              {errors.unit_price && (
                <p className="mt-1 text-sm text-red-600">
                  {errors.unit_price.message}
                </p>
              )}
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700">
                Notes
              </label>
              <textarea
                {...register("notes")}
                className="mt-1 block w-full rounded-md border border-gray-300 py-2 px-3 shadow-sm focus:border-indigo-500 focus:outline-none focus:ring-indigo-500"
              />
            </div>

            <div className="mt-4 flex justify-end space-x-2">
              <Button type="button" variant="outline" onClick={onClose}>
                Cancel
              </Button>
              <Button type="submit">Create Sale</Button>
            </div>
          </form>
        </div>
      </div>
    </Dialog>
  );
}
