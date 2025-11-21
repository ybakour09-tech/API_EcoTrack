export type UserRole = "user" | "admin";

export type AuthState = {
  token: string | null;
  user: { id: number; email: string; role: UserRole } | null;
};

export type LoginPayload = {
  email: string;
  password: string;
};

export type Indicator = {
  id: number;
  type: string;
  value: number;
  unit: string;
  timestamp: string;
  zone_id: number;
  source_id: number | null;
  zone?: { id: number; name: string };
  source?: { id: number; name: string };
};

export type PaginatedIndicators = {
  total: number;
  items: Indicator[];
};

export type Zone = {
  id: number;
  name: string;
  postal_code?: string;
  latitude?: number;
  longitude?: number;
  description?: string;
};

export type Source = {
  id: number;
  name: string;
  url?: string;
  description?: string;
};

export type User = {
  id: number;
  email: string;
  full_name?: string;
  role: UserRole;
  is_active: boolean;
};

export type TrendPoint = {
  bucket: string;
  value: number;
};

