import { CalendarDays, LogOut } from "lucide-react";
import { useNavigate } from "react-router-dom";

import { useAuth } from "../../context/AuthProvider";
import { Button } from "../ui/Button";

export const Topbar = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  return (
    <header className="flex flex-col gap-4 border-b border-amber-100/60 bg-white/90 px-5 py-4 text-slate-700 shadow-soft backdrop-blur-xl lg:flex-row lg:items-center lg:justify-between lg:px-10 animate-slide-up">
      <div>
        <p className="text-lg font-bold text-slate-900">
          Bonjour, <span className="text-brand-dark">{user?.email ?? "EcoTrack"}</span>
        </p>
        <p className="text-xs font-medium text-slate-500 mt-0.5">Vision d'ensemble en temps réel</p>
      </div>
      <div className="flex flex-wrap items-center gap-3 text-sm text-slate-500">
        <span className="hidden items-center gap-2 rounded-full border border-amber-100/80 bg-gradient-to-r from-amber-50/90 to-white/90 px-4 py-2 font-medium text-slate-700 shadow-sm md:flex transition-all duration-200 hover:shadow-md hover:scale-[1.02]">
          <CalendarDays size={16} className="text-brand-dark" />
          {new Date().toLocaleDateString("fr-FR", {
            weekday: "long",
            day: "2-digit",
            month: "long"
          })}
        </span>
        <Button
          variant="ghost"
          className="gap-2 border-brand/30 text-brand-dark hover:bg-gradient-to-r hover:from-brand/10 hover:to-transparent hover:border-brand/40 hover:shadow-sm transition-all duration-200"
          onClick={() => {
            logout();
            navigate("/login");
          }}
        >
          <LogOut size={16} />
          Déconnexion
        </Button>
      </div>
    </header>
  );
};

