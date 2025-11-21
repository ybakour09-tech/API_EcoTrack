import { BookMarked } from "lucide-react";

import { Card } from "../components/ui/Card";
import { useSources } from "../hooks/useApi";

export const SourcesPage = () => {
  const { data, isLoading } = useSources();

  return (
    <div className="space-y-6 animate-fade-in">
      <div>
        <h1 className="text-2xl font-bold text-slate-900">Sources</h1>
        <p className="text-xs font-medium text-slate-500 mt-1">
          Liste des APIs / datasets intégrés
        </p>
      </div>

      <Card title="Catalogue" className="animate-slide-up">
        {isLoading && (
          <div className="flex items-center justify-center py-8">
            <p className="text-sm font-medium text-slate-500">Chargement...</p>
          </div>
        )}
        <div className="space-y-3">
          {data?.map((source, index) => (
            <div
              key={source.id}
              className="flex flex-col gap-2 rounded-xl border border-amber-100/60 bg-gradient-to-br from-white/90 to-amber-50/30 p-5 shadow-sm transition-all duration-200 hover:shadow-md hover:scale-[1.01] animate-slide-up"
              style={{ animationDelay: `${index * 50}ms` }}
            >
              <div className="flex items-center gap-2 text-lg font-bold text-slate-900">
                <BookMarked size={18} className="text-brand-dark" />
                {source.name}
              </div>
              <p className="text-sm font-medium text-slate-600">{source.description ?? "—"}</p>
              {source.url && (
                <a
                  href={source.url}
                  target="_blank"
                  rel="noreferrer"
                  className="text-xs font-semibold text-brand-dark underline hover:text-brand transition-colors"
                >
                  {source.url}
                </a>
              )}
            </div>
          ))}
        </div>
      </Card>
    </div>
  );
};

