import React from "react";
import { Dialog } from "@headlessui/react";
import { useForm } from "react-hook-form";
import { useMutation, useQueryClient, useQuery } from "@tanstack/react-query";
import { toast } from "react-toastify";
import { createProduct, updateProduct } from "@/services/products";
import type {
  Product,
  CreateProductDTO,
  Category,
  Supplier,
} from "@/services/products";
import { api } from "@/lib/axios";

interface ProductModalProps {
  isOpen: boolean;
  onClose: () => void;
  product: Product | null;
}

export default function ProductModal({
  isOpen,
  onClose,
  product,
}: ProductModalProps) {
  const queryClient = useQueryClient();

  // Add queries for categories and suppliers
  const { data: categories = [] } = useQuery<Category[]>({
    queryKey: ["categories"],
    queryFn: async () => {
      const response = await api.get("/categories");
      return response.data;
    },
  });

  const { data: suppliers = [] } = useQuery<Supplier[]>({
    queryKey: ["suppliers"],
    queryFn: async () => {
      const response = await api.get("/suppliers");
      return response.data;
    },
  });

  const {
    register,
    handleSubmit,
    reset,
    formState: { errors },
  } = useForm<CreateProductDTO>({
    defaultValues: product
      ? {
          name: product.name,
          description: product.description || "",
          sku: product.sku,
          barcode: product.barcode || "",
          price: product.price,
          cost: product.cost,
          stock: product.stock,
          min_quantity: product.min_quantity,
          category_id: product.category_id,
          supplier_id: product.supplier_id,
        }
      : {
          name: "",
          description: "",
          sku: "",
          barcode: "",
          price: 0,
          cost: 0,
          stock: 0,
          min_quantity: 0,
          category_id: categories[0]?.id,
          supplier_id: suppliers[0]?.id,
        },
  });

  React.useEffect(() => {
    if (isOpen) {
      reset(
        product
          ? {
              name: product.name,
              description: product.description || "",
              sku: product.sku,
              barcode: product.barcode || "",
              price: product.price,
              cost: product.cost,
              stock: product.stock,
              min_quantity: product.min_quantity,
              category_id: product.category_id,
              supplier_id: product.supplier_id,
            }
          : {
              name: "",
              description: "",
              sku: "",
              barcode: "",
              price: 0,
              cost: 0,
              stock: 0,
              min_quantity: 0,
              category_id: categories[0]?.id,
              supplier_id: suppliers[0]?.id,
            }
      );
    }
  }, [isOpen, product, reset, categories, suppliers]);

  const createMutation = useMutation({
    mutationFn: createProduct,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["products"] });
      toast.success("Product created successfully");
      onClose();
      reset();
    },
    onError: (error: Error) => {
      toast.error(error.message || "Failed to create product");
    },
  });

  const updateMutation = useMutation({
    mutationFn: ({
      id,
      data,
    }: {
      id: number;
      data: Partial<CreateProductDTO>;
    }) => updateProduct(id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["products"] });
      toast.success("Product updated successfully");
      onClose();
    },
    onError: (error: Error) => {
      toast.error(error.message || "Failed to update product");
    },
  });

  const onSubmit = (data: CreateProductDTO) => {
    // Convert string values to numbers for numeric fields and ensure they are positive
    const formattedData = {
      ...data,
      price: Math.max(0.01, Number(data.price)),
      cost: Math.max(0.01, Number(data.cost)),
      stock: Math.max(0, Number(data.stock)),
      min_quantity: Math.max(0, Number(data.min_quantity)),
      category_id: Number(data.category_id),
      supplier_id: Number(data.supplier_id),
    };

    if (product) {
      // When updating, only include non-null and non-undefined values
      const updateData = Object.fromEntries(
        Object.entries(formattedData).filter(([_, value]) => value != null)
      ) as Partial<CreateProductDTO>;
      updateMutation.mutate({ id: product.id, data: updateData });
    } else {
      createMutation.mutate(formattedData);
    }
  };

  return (
    <Dialog open={isOpen} onClose={onClose} className="relative z-50">
      <div className="fixed inset-0 bg-black/30" aria-hidden="true" />
      <div className="fixed inset-0 flex items-center justify-center p-4">
        <Dialog.Panel className="mx-auto max-w-xl rounded bg-white p-6">
          <Dialog.Title className="text-lg font-medium leading-6 text-gray-900">
            {product ? "Edit Product" : "Add Product"}
          </Dialog.Title>

          <form onSubmit={handleSubmit(onSubmit)} className="mt-4 space-y-4">
            <div>
              <label
                htmlFor="name"
                className="block text-sm font-medium text-gray-700"
              >
                Name
              </label>
              <input
                type="text"
                {...register("name", { required: "Name is required" })}
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
              />
              {errors.name && (
                <p className="mt-1 text-sm text-red-600">
                  {errors.name.message}
                </p>
              )}
            </div>

            <div>
              <label
                htmlFor="sku"
                className="block text-sm font-medium text-gray-700"
              >
                SKU
              </label>
              <input
                type="text"
                {...register("sku", { required: "SKU is required" })}
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
              />
              {errors.sku && (
                <p className="mt-1 text-sm text-red-600">
                  {errors.sku.message}
                </p>
              )}
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label
                  htmlFor="price"
                  className="block text-sm font-medium text-gray-700"
                >
                  Price
                </label>
                <input
                  type="number"
                  step="0.01"
                  min="0.01"
                  {...register("price", {
                    required: "Price is required",
                    min: {
                      value: 0.01,
                      message: "Price must be greater than 0",
                    },
                    valueAsNumber: true,
                  })}
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
                />
                {errors.price && (
                  <p className="mt-1 text-sm text-red-600">
                    {errors.price.message}
                  </p>
                )}
              </div>

              <div>
                <label
                  htmlFor="cost"
                  className="block text-sm font-medium text-gray-700"
                >
                  Cost
                </label>
                <input
                  type="number"
                  step="0.01"
                  min="0.01"
                  {...register("cost", {
                    required: "Cost is required",
                    min: {
                      value: 0.01,
                      message: "Cost must be greater than 0",
                    },
                    valueAsNumber: true,
                  })}
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
                />
                {errors.cost && (
                  <p className="mt-1 text-sm text-red-600">
                    {errors.cost.message}
                  </p>
                )}
              </div>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label
                  htmlFor="stock"
                  className="block text-sm font-medium text-gray-700"
                >
                  Stock
                </label>
                <input
                  type="number"
                  min="0"
                  step="1"
                  {...register("stock", {
                    required: "Stock is required",
                    min: { value: 0, message: "Stock must be 0 or greater" },
                    valueAsNumber: true,
                  })}
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
                />
                {errors.stock && (
                  <p className="mt-1 text-sm text-red-600">
                    {errors.stock.message}
                  </p>
                )}
              </div>

              <div>
                <label
                  htmlFor="min_quantity"
                  className="block text-sm font-medium text-gray-700"
                >
                  Min Quantity
                </label>
                <input
                  type="number"
                  min="0"
                  step="1"
                  {...register("min_quantity", {
                    required: "Min quantity is required",
                    min: {
                      value: 0,
                      message: "Min quantity must be 0 or greater",
                    },
                    valueAsNumber: true,
                  })}
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
                />
                {errors.min_quantity && (
                  <p className="mt-1 text-sm text-red-600">
                    {errors.min_quantity.message}
                  </p>
                )}
              </div>
            </div>

            <div>
              <label
                htmlFor="description"
                className="block text-sm font-medium text-gray-700"
              >
                Description
              </label>
              <textarea
                {...register("description")}
                rows={3}
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
              />
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label
                  htmlFor="category_id"
                  className="block text-sm font-medium text-gray-700"
                >
                  Category
                </label>
                <select
                  {...register("category_id", {
                    required: "Category is required",
                  })}
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
                >
                  <option value="">Select a category</option>
                  {categories.map((category) => (
                    <option key={category.id} value={category.id}>
                      {category.name}
                    </option>
                  ))}
                </select>
                {errors.category_id && (
                  <p className="mt-1 text-sm text-red-600">
                    {errors.category_id.message}
                  </p>
                )}
              </div>

              <div>
                <label
                  htmlFor="supplier_id"
                  className="block text-sm font-medium text-gray-700"
                >
                  Supplier
                </label>
                <select
                  {...register("supplier_id", {
                    required: "Supplier is required",
                  })}
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
                >
                  <option value="">Select a supplier</option>
                  {suppliers.map((supplier) => (
                    <option key={supplier.id} value={supplier.id}>
                      {supplier.name}
                    </option>
                  ))}
                </select>
                {errors.supplier_id && (
                  <p className="mt-1 text-sm text-red-600">
                    {errors.supplier_id.message}
                  </p>
                )}
              </div>
            </div>

            <div className="mt-5 sm:mt-6 sm:grid sm:grid-flow-row-dense sm:grid-cols-2 sm:gap-3">
              <button
                type="submit"
                className="inline-flex w-full justify-center rounded-md border border-transparent bg-indigo-600 px-4 py-2 text-base font-medium text-white shadow-sm hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 sm:col-start-2 sm:text-sm"
              >
                {product ? "Update" : "Create"}
              </button>
              <button
                type="button"
                onClick={onClose}
                className="mt-3 inline-flex w-full justify-center rounded-md border border-gray-300 bg-white px-4 py-2 text-base font-medium text-gray-700 shadow-sm hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 sm:col-start-1 sm:mt-0 sm:text-sm"
              >
                Cancel
              </button>
            </div>
          </form>
        </Dialog.Panel>
      </div>
    </Dialog>
  );
}
