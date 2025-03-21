import { api } from "@/lib/axios";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8001";

export interface LoginResponse {
  access_token: string;
  token_type: string;
}

export interface User {
  id: number;
  email: string;
  full_name: string;
  is_active: boolean;
  is_superuser: boolean;
}

export interface LoginCredentials {
  email: string;
  password: string;
}

export interface RegisterCredentials {
  email: string;
  password: string;
  fullName: string;
}

export async function login(
  credentials: LoginCredentials
): Promise<{ access_token: string; token_type: string; user: User }> {
  try {
    console.log("Attempting login with:", credentials.email);
    const formData = new URLSearchParams();
    formData.append("username", credentials.email);
    formData.append("password", credentials.password);

    const response = await api.post<LoginResponse>(
      "/login/access-token",
      formData,
      {
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
      }
    );
    console.log("Login successful:", response.data);

    // Set the token for subsequent requests
    localStorage.setItem("token", response.data.access_token);

    // Get user info
    const userResponse = await api.get<User>("/users/me", {
      headers: {
        Authorization: `Bearer ${response.data.access_token}`,
      },
    });

    return {
      ...response.data,
      user: userResponse.data,
    };
  } catch (error) {
    console.error("Login error:", error);
    if (error instanceof Error) {
      throw new Error(error.message || "Login failed");
    }
    throw error;
  }
}

export async function register(
  credentials: RegisterCredentials
): Promise<{ access_token: string; token_type: string; user: User }> {
  try {
    console.log("Attempting registration with:", credentials.email);
    // First register the user
    const registerResponse = await api.post<User>("/users/register", {
      email: credentials.email,
      password: credentials.password,
      full_name: credentials.fullName,
    });
    console.log("Registration successful:", registerResponse.data);

    // Then login to get the token
    return login({
      email: credentials.email,
      password: credentials.password,
    });
  } catch (error) {
    console.error("Registration error:", error);
    if (error instanceof Error) {
      const errorMessage = error.message || "Registration failed";
      console.error("Registration error details:", errorMessage);
      throw new Error(errorMessage);
    }
    throw error;
  }
}

export async function getCurrentUser() {
  try {
    console.log("Fetching current user");
    const response = await api.get<User>("/users/me");
    console.log("Current user:", response.data);
    return response.data;
  } catch (error) {
    console.error("Get current user error:", error);
    if (error instanceof Error) {
      throw new Error(error.message || "Failed to get current user");
    }
    throw error;
  }
}

// Add axios interceptor for handling authentication
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});
