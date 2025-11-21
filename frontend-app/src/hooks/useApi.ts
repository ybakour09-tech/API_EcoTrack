import { useMutation, useQuery } from "@tanstack/react-query";

import { apiClient } from "../services/api";
import type {
  PaginatedIndicators,
  Source,
  TrendPoint,
  User,
  Zone
} from "../types";

export const useIndicators = (params: Record<string, string | number | undefined>) =>
  useQuery({
    queryKey: ["indicators", params],
    queryFn: async () => {
      const response = await apiClient.get<PaginatedIndicators>("/indicators", {
        params
      });
      return response.data;
    }
  });

export const useTrend = (params: { zone_id: number; indicator_type: string; period?: string }) =>
  useQuery({
    queryKey: ["trend", params],
    queryFn: async () => {
      const response = await apiClient.get<{ series: TrendPoint[] }>("/stats/trend", { params });
      return response.data.series;
    },
    enabled: Boolean(params.zone_id && params.indicator_type)
  });

export const useAirAverage = (params: { zone_id?: number; indicator_type?: string }) =>
  useQuery({
    queryKey: ["air-average", params],
    queryFn: async () => {
      const response = await apiClient.get("/stats/air/averages", { params });
      return response.data;
    }
  });

export const useZones = () =>
  useQuery({
    queryKey: ["zones"],
    queryFn: async () => {
      const response = await apiClient.get<Zone[]>("/zones");
      return response.data;
    }
  });

export const useSources = () =>
  useQuery({
    queryKey: ["sources"],
    queryFn: async () => {
      const response = await apiClient.get<Source[]>("/sources");
      return response.data;
    }
  });

export const useUsers = () =>
  useQuery({
    queryKey: ["users"],
    queryFn: async () => {
      const response = await apiClient.get<User[]>("/users");
      return response.data;
    }
  });

export const useCreateZone = () =>
  useMutation({
    mutationFn: async (payload: Partial<Zone>) => {
      const response = await apiClient.post<Zone>("/zones", payload);
      return response.data;
    }
  });

