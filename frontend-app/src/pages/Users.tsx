import { Shield } from "lucide-react";

import { Card } from "../components/ui/Card";
import { useUsers } from "../hooks/useApi";

export const UsersPage = () => {
  const { data, isLoading } = useUsers();

  return (
    <div className="space-y-6 animate-fade-in">
      <div>
        <h1 className="text-2xl font-bold text-slate-900">Utilisateurs</h1>
        <p className="text-xs font-medium text-slate-500 mt-1">
          Gestion des accès et des rôles (admin only)
        </p>
      </div>

      <Card title="Liste des utilisateurs" className="animate-slide-up">
        {isLoading && (
          <div className="flex items-center justify-center py-8">
            <p className="text-sm font-medium text-slate-500">Chargement...</p>
          </div>
        )}
        <div className="space-y-3">
          {data?.map((user, index) => (
            <div
              key={user.id}
              className="flex items-center justify-between rounded-xl border border-amber-100/60 bg-gradient-to-r from-white/90 to-amber-50/30 px-5 py-3.5 shadow-sm transition-all duration-200 hover:shadow-md hover:scale-[1.01] animate-slide-up"
              style={{ animationDelay: `${index * 50}ms` }}
            >
              <div>
                <p className="font-bold text-slate-900">{user.email}</p>
                <p className="text-xs font-medium text-slate-500 mt-0.5">
                  {user.full_name ?? "Nom non renseigné"}
                </p>
              </div>
              <div className="flex items-center gap-2 rounded-full border border-brand/20 bg-brand/10 px-3 py-1.5 text-xs font-bold text-brand-dark">
                <Shield size={14} />
                {user.role}
              </div>
            </div>
          ))}
        </div>
      </Card>
    </div>
  );
};

