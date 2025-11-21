import { Link } from "react-router-dom";
import {
  ChartLine,
  Database,
  Gauge,
  Layers,
  MapPin,
  Users
} from "lucide-react";
import clsx from "classnames";

type SidebarProps = {
  currentPath: string;
};

const links = [
  { to: "/", label: "Dashboard", icon: Gauge },
  { to: "/indicators", label: "Indicateurs", icon: Database },
  { to: "/stats", label: "Statistiques", icon: ChartLine },
  { to: "/users", label: "Utilisateurs", icon: Users },
  { to: "/zones", label: "Zones", icon: MapPin },
  { to: "/sources", label: "Sources", icon: Layers }
];

export const Sidebar = ({ currentPath }: SidebarProps) => {
  return (
    <aside className="hidden w-72 flex-col border-r border-amber-100/60 bg-white/85 pb-8 pt-6 shadow-2xl shadow-amber-100/50 backdrop-blur-2xl lg:flex animate-fade-in">
      <div className="border-b border-amber-100/60 px-6 pb-5">
        <p className="text-xl font-bold gradient-text">EcoTrack</p>
        <p className="text-xs font-medium text-slate-500 mt-1">Monitoring environnemental</p>
      </div>
      <nav className="flex-1 space-y-1.5 px-4 py-6 text-sm">
        {links.map(({ to, label, icon: Icon }, index) => {
          const active = currentPath === to || currentPath.startsWith(`${to}/`);
          return (
            <Link
              key={to}
              to={to}
              className={clsx(
                "flex items-center gap-3 rounded-xl px-4 py-2.5 font-semibold transition-all duration-200 animate-slide-up",
                "hover:scale-[1.02] active:scale-[0.98]",
                active
                  ? "bg-gradient-to-r from-brand/25 via-brand/15 to-brand/5 text-brand-dark shadow-md shadow-brand/20 border border-brand/20"
                  : "text-slate-600 hover:bg-gradient-to-r hover:from-amber-50/80 hover:to-transparent hover:text-slate-900 hover:shadow-sm"
              )}
              style={{ animationDelay: `${index * 50}ms` }}
            >
              <Icon size={18} className={active ? "text-brand-dark" : ""} />
              {label}
            </Link>
          );
        })}
      </nav>
    </aside>
  );
};

