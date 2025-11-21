import { Outlet, useLocation } from "react-router-dom";

import { Sidebar } from "./components/layout/Sidebar";
import { Topbar } from "./components/layout/Topbar";

export const AppShell = () => {
  const location = useLocation();

  return (
    <div className="flex min-h-screen bg-[#fdfbf4] text-slate-900">
      <Sidebar currentPath={location.pathname} />
      <main className="flex flex-1 flex-col">
        <Topbar />
        <div className="flex-1 overflow-y-auto px-4 py-6 lg:px-12 animate-fade-in">
          <Outlet />
        </div>
      </main>
    </div>
  );
};

