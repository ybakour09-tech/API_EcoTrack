import { useMemo, useState } from "react";
import { Filter, RefreshCw } from "lucide-react";

import { Card } from "../components/ui/Card";
import { Button } from "../components/ui/Button";
import { IndicatorsTable } from "../components/tables/IndicatorsTable";
import { TrendChart } from "../components/charts/TrendChart";
import {
  useAirAverage,
  useIndicators,
  useTrend,
  useZones
} from "../hooks/useApi";

export const DashboardPage = () => {
  const { data: zones } = useZones();
  const [filters, setFilters] = useState<{ zone_id?: number; type?: string }>({});
  const { data, isLoading, refetch } = useIndicators({
    limit: 8,
    zone_id: filters.zone_id,
    indicator_type: filters.type
  });
  const trendZone = filters.zone_id ?? zones?.[0]?.id;
  const { data: trend } = useTrend({
    zone_id: trendZone ?? 0,
    indicator_type: filters.type ?? "pm25",
    period: "monthly"
  });
  const { data: averages } = useAirAverage({
    zone_id: trendZone,
    indicator_type: filters.type ?? "pm25"
  });

  const statCards = useMemo(
    () => [
      {
        label: "Moyenne",
        value: averages?.average ? averages.average.toFixed(1) : "—",
        suffix: "µg/m³"
      },
      {
        label: "Période",
        value: averages?.start
          ? new Date(averages.start).toLocaleDateString("fr-FR")
          : "—",
        suffix: averages?.end
          ? `→ ${new Date(averages.end).toLocaleDateString("fr-FR")}`
          : ""
      },
      {
        label: "Zone",
        value:
          zones?.find((zone) => zone.id === trendZone)?.name ??
          "Toutes les zones",
        suffix: ""
      }
    ],
    [averages, zones, trendZone]
  );

  return (
    <div className="space-y-6">
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-slate-900">Dashboard</h1>
          <p className="text-xs font-medium text-slate-500 mt-1">
            Résumé des indicateurs clés en temps réel
          </p>
        </div>
        <div className="flex gap-3">
          <Button variant="ghost" onClick={() => refetch()}>
            <RefreshCw size={16} className="mr-2" />
            Actualiser
          </Button>
          <Button
            variant="ghost"
            onClick={() => setFilters({})}
          >
            Réinitialiser
          </Button>
        </div>
      </div>

      <div className="grid gap-4 md:grid-cols-3">
        {statCards.map((card, index) => (
          <Card key={card.label} className="animate-slide-up" style={{ animationDelay: `${index * 100}ms` }}>
            <p className="text-xs font-bold uppercase tracking-wider text-slate-500">{card.label}</p>
            <p className="mt-3 text-3xl font-bold text-slate-900">
              {card.value}{" "}
              <span className="text-base font-semibold text-slate-500">
                {card.suffix}
              </span>
            </p>
          </Card>
        ))}
      </div>

      <div className="grid gap-4 lg:grid-cols-3">
        <Card className="lg:col-span-2" title="Tendance mensuelle">
          {trend && trend.length > 0 ? (
            <TrendChart data={trend} />
          ) : (
            <p className="text-sm text-slate-500">
              Pas de données suffisantes pour cette combinaison.
            </p>
          )}
        </Card>
        <Card
          title="Filtres"
          actions={
            <Filter size={16} className="text-slate-500" />
          }
        >
          <div className="space-y-4">
            <div>
              <label className="text-sm text-slate-500">Zone</label>
              <select
                className="form-field mt-1"
                value={filters.zone_id ?? ""}
                onChange={(e) =>
                  setFilters((prev) => ({
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
              <label className="text-sm text-slate-500">Type</label>
              <input
                className="form-field mt-1"
                placeholder="pm25, co2..."
                value={filters.type ?? ""}
                onChange={(e) =>
                  setFilters((prev) => ({
                    ...prev,
                    type: e.target.value || undefined
                  }))
                }
              />
            </div>
          </div>
        </Card>
      </div>

      <Card title="Flux récents">
        {isLoading && <p className="text-sm text-slate-500">Chargement...</p>}
        {data && <IndicatorsTable data={data.items} />}
      </Card>
    </div>
  );
};

