import { useMemo, useState } from "react";
import { ArrowUpRight } from "lucide-react";

import { Card } from "../components/ui/Card";
import { TrendChart } from "../components/charts/TrendChart";
import { useTrend, useZones } from "../hooks/useApi";

export const StatsPage = () => {
  const { data: zones } = useZones();
  const [params, setParams] = useState({
    zone_id: undefined as number | undefined,
    indicator_type: "pm25",
    period: "monthly"
  });
  const { data, isLoading } = useTrend({
    zone_id: params.zone_id ?? zones?.[0]?.id ?? 0,
    indicator_type: params.indicator_type,
    period: params.period
  });

  const insights = useMemo(() => {
    if (!data || data.length < 2) return [];
    const latest = data[data.length - 1];
    const previous = data[data.length - 2];
    const variation = latest.value - previous.value;
    return [
      {
        label: "Variation récente",
        value: `${variation > 0 ? "+" : ""}${variation.toFixed(2)}`,
        trend: variation >= 0 ? "hausse" : "baisse"
      },
      {
        label: "Valeur max",
        value: Math.max(...data.map((d) => d.value)).toFixed(2)
      },
      {
        label: "Valeur min",
        value: Math.min(...data.map((d) => d.value)).toFixed(2)
      }
    ];
  }, [data]);

  return (
    <div className="space-y-6 animate-fade-in">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-slate-900">Statistiques</h1>
          <p className="text-xs font-medium text-slate-500 mt-1">
            Analyse temporelle des indicateurs par zone
          </p>
        </div>
      </div>

      <Card title="Paramètres d'analyse" className="animate-slide-up">
        <div className="grid gap-4 md:grid-cols-3">
          <div>
            <label className="text-xs font-semibold uppercase tracking-wide text-slate-600 mb-2 block">
              Zone
            </label>
            <select
              className="form-field"
              value={params.zone_id ?? ""}
              onChange={(e) =>
                setParams((prev) => ({
                  ...prev,
                  zone_id: e.target.value ? Number(e.target.value) : undefined
                }))
              }
            >
              <option value="">Toutes</option>
              {zones?.map((zone) => (
                <option key={zone.id} value={zone.id}>
                  {zone.name}
                </option>
              ))}
            </select>
          </div>
          <div>
            <label className="text-xs font-semibold uppercase tracking-wide text-slate-600 mb-2 block">
              Type
            </label>
            <input
              className="form-field"
              value={params.indicator_type}
              onChange={(e) =>
                setParams((prev) => ({ ...prev, indicator_type: e.target.value }))
              }
            />
          </div>
          <div>
            <label className="text-xs font-semibold uppercase tracking-wide text-slate-600 mb-2 block">
              Période
            </label>
            <select
              className="form-field"
              value={params.period}
              onChange={(e) =>
                setParams((prev) => ({ ...prev, period: e.target.value as "daily" | "weekly" | "monthly" }))
              }
            >
              <option value="daily">Journalier</option>
              <option value="weekly">Hebdo</option>
              <option value="monthly">Mensuel</option>
            </select>
          </div>
        </div>
      </Card>

      <div className="grid gap-4 lg:grid-cols-3">
        <Card className="lg:col-span-2 animate-slide-up" style={{ animationDelay: "100ms" }}>
          {isLoading && (
            <div className="flex items-center justify-center py-8">
              <p className="text-sm font-medium text-slate-500">Chargement...</p>
            </div>
          )}
          {data && <TrendChart data={data} />}
        </Card>
        <div className="space-y-4">
          {insights.map((insight, index) => (
            <Card key={insight.label} className="animate-slide-up" style={{ animationDelay: `${(index + 1) * 100}ms` }}>
              <p className="text-xs font-bold uppercase tracking-wider text-slate-500">{insight.label}</p>
              <p className="mt-3 flex items-center gap-2 text-3xl font-bold text-slate-900">
                {insight.value}
                <ArrowUpRight size={18} className="text-brand-dark" />
              </p>
              {insight.trend && (
                <p className="text-xs font-medium text-slate-500 mt-2">
                  Tendance actuelle : <span className="text-brand-dark font-semibold">{insight.trend}</span>
                </p>
              )}
            </Card>
          ))}
        </div>
      </div>
    </div>
  );
};

