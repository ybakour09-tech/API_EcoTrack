import { useState } from "react";
import { Plus } from "lucide-react";

import { Card } from "../components/ui/Card";
import { Button } from "../components/ui/Button";
import { IndicatorsTable } from "../components/tables/IndicatorsTable";
import { useIndicators } from "../hooks/useApi";

export const IndicatorsPage = () => {
  const [filters, setFilters] = useState<{ type?: string; zone_id?: number }>({});
  const { data, isLoading } = useIndicators({
    ...filters,
    limit: 50
  });

  return (
    <div className="space-y-6 animate-fade-in">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <div>
          <h1 className="text-2xl font-bold text-slate-900">Indicateurs</h1>
          <p className="text-xs font-medium text-slate-500 mt-1">
            Liste complète avec filtres avancés
          </p>
        </div>
        <Button className="animate-scale-in">
          <Plus size={16} className="mr-2" />
          Ajouter
        </Button>
      </div>

      <Card title="Filtres" className="animate-slide-up">
        <div className="grid gap-4 md:grid-cols-3">
          <div>
            <label className="text-xs font-semibold uppercase tracking-wide text-slate-600 mb-2 block">
              Type
            </label>
            <input
              className="form-field"
              placeholder="pm25, co2..."
              value={filters.type ?? ""}
              onChange={(e) =>
                setFilters((prev) => ({ ...prev, type: e.target.value || undefined }))
              }
            />
          </div>
          <div>
            <label className="text-xs font-semibold uppercase tracking-wide text-slate-600 mb-2 block">
              Zone ID
            </label>
            <input
              type="number"
              className="form-field"
              value={filters.zone_id ?? ""}
              onChange={(e) =>
                setFilters((prev) => ({
                  ...prev,
                  zone_id: e.target.value ? Number(e.target.value) : undefined
                }))
              }
            />
          </div>
          <div className="flex items-end">
            <Button
              variant="ghost"
              className="w-full justify-center"
              onClick={() => setFilters({})}
            >
              Réinitialiser
            </Button>
          </div>
        </div>
      </Card>

      <Card title="Résultats" className="animate-slide-up" style={{ animationDelay: "100ms" }}>
        {isLoading && (
          <div className="flex items-center justify-center py-8">
            <p className="text-sm font-medium text-slate-500">Chargement...</p>
          </div>
        )}
        {data && <IndicatorsTable data={data.items} />}
      </Card>
    </div>
  );
};

