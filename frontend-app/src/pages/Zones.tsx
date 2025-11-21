import { useState } from "react";
import { MapPinned } from "lucide-react";
import { useQueryClient } from "@tanstack/react-query";

import { Card } from "../components/ui/Card";
import { Button } from "../components/ui/Button";
import { useCreateZone, useZones } from "../hooks/useApi";

export const ZonesPage = () => {
  const queryClient = useQueryClient();
  const { data, isLoading } = useZones();
  const createZone = useCreateZone();
  const [form, setForm] = useState({
    name: "",
    postal_code: "",
    description: ""
  });

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    await createZone.mutateAsync({
      name: form.name,
      postal_code: form.postal_code,
      description: form.description
    });
    await queryClient.invalidateQueries({ queryKey: ["zones"] });
    setForm({ name: "", postal_code: "", description: "" });
  };

  return (
    <div className="space-y-6 animate-fade-in">
      <div>
        <h1 className="text-2xl font-bold text-slate-900">Zones géographiques</h1>
        <p className="text-xs font-medium text-slate-500 mt-1">
          Cartographiez vos périmètres de suivi
        </p>
      </div>

      <Card title="Créer une zone" className="animate-slide-up">
        <form className="grid gap-4 md:grid-cols-3" onSubmit={handleSubmit}>
          <div>
            <label className="text-xs font-semibold uppercase tracking-wide text-slate-600 mb-2 block">
              Nom
            </label>
            <input
              className="form-field"
              value={form.name}
              onChange={(e) => setForm((prev) => ({ ...prev, name: e.target.value }))}
              required
            />
          </div>
          <div>
            <label className="text-xs font-semibold uppercase tracking-wide text-slate-600 mb-2 block">
              Code postal
            </label>
            <input
              className="form-field"
              value={form.postal_code}
              onChange={(e) =>
                setForm((prev) => ({ ...prev, postal_code: e.target.value }))
              }
            />
          </div>
          <div>
            <label className="text-xs font-semibold uppercase tracking-wide text-slate-600 mb-2 block">
              Description
            </label>
            <input
              className="form-field"
              value={form.description}
              onChange={(e) =>
                setForm((prev) => ({ ...prev, description: e.target.value }))
              }
            />
          </div>
          <div className="flex justify-end md:col-span-3">
            <Button type="submit" className="w-full md:w-auto">
              Ajouter
            </Button>
          </div>
        </form>
      </Card>

      <Card title="Liste des zones" className="animate-slide-up" style={{ animationDelay: "100ms" }}>
        {isLoading && (
          <div className="flex items-center justify-center py-8">
            <p className="text-sm font-medium text-slate-500">Chargement...</p>
          </div>
        )}
        <div className="grid gap-4 md:grid-cols-2">
          {data?.map((zone, index) => (
            <div
              key={zone.id}
              className="rounded-xl border border-amber-100/60 bg-gradient-to-br from-white/90 to-amber-50/30 p-5 shadow-sm transition-all duration-200 hover:shadow-md hover:scale-[1.02] animate-slide-up"
              style={{ animationDelay: `${index * 50}ms` }}
            >
              <div className="flex items-center gap-2 font-bold text-slate-900 mb-2">
                <MapPinned size={18} className="text-brand-dark" />
                {zone.name}
              </div>
              <p className="text-xs font-medium text-slate-600 mb-2">{zone.description ?? "—"}</p>
              <p className="text-xs font-semibold text-slate-500">
                {zone.postal_code ?? "Code postal inconnu"}
              </p>
            </div>
          ))}
        </div>
      </Card>
    </div>
  );
};

