import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useState
} from "react";
import { apiClient } from "../services/api";
import type { AuthState, LoginPayload } from "../types";

type AuthContextValue = AuthState & {
  login: (payload: LoginPayload) => Promise<void>;
  logout: () => void;
};

const AuthContext = createContext<AuthContextValue | undefined>(undefined);
const STORAGE_KEY = "ecotrack_auth";

export const AuthProvider = ({ children }: { children: React.ReactNode }) => {
  const [state, setState] = useState<AuthState>(() => {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) {
      return { token: null, user: null };
    }
    try {
      return JSON.parse(raw);
    } catch {
      return { token: null, user: null };
    }
  });

  useEffect(() => {
    if (state.token) {
      apiClient.defaults.headers.common.Authorization = `Bearer ${state.token}`;
    } else {
      delete apiClient.defaults.headers.common.Authorization;
    }
    localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
  }, [state]);

  const login = useCallback(async (payload: LoginPayload) => {
    const data = new URLSearchParams();
    data.set("username", payload.email);
    data.set("password", payload.password);

    const response = await apiClient.post("/auth/login", data, {
      headers: { "Content-Type": "application/x-www-form-urlencoded" }
    });

    setState({
      token: response.data.token.access_token,
      user: {
        email: response.data.email,
        role: response.data.role,
        id: response.data.user_id
      }
    });
  }, []);

  const logout = useCallback(() => {
    setState({ token: null, user: null });
    localStorage.removeItem(STORAGE_KEY);
  }, []);

  const value = useMemo(
    () => ({
      ...state,
      login,
      logout
    }),
    [state, login, logout]
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within AuthProvider");
  }
  return context;
};

