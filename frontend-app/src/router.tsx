import { createBrowserRouter, Navigate } from "react-router-dom";

import { AppShell } from "./App";
import { DashboardPage } from "./pages/Dashboard";
import { IndicatorsPage } from "./pages/Indicators";
import { StatsPage } from "./pages/Stats";
import { UsersPage } from "./pages/Users";
import { ZonesPage } from "./pages/Zones";
import { SourcesPage } from "./pages/Sources";
import { LoginPage } from "./pages/Login";
import { RequireAuth } from "./components/layout/RequireAuth";

export const router = createBrowserRouter([
  {
    path: "/login",
    element: <LoginPage />
  },
  {
    path: "/",
    element: (
      <RequireAuth>
        <AppShell />
      </RequireAuth>
    ),
    children: [
      { index: true, element: <DashboardPage /> },
      { path: "indicators", element: <IndicatorsPage /> },
      { path: "stats", element: <StatsPage /> },
      { path: "users", element: <UsersPage /> },
      { path: "zones", element: <ZonesPage /> },
      { path: "sources", element: <SourcesPage /> },
      { path: "*", element: <Navigate to="/" replace /> }
    ]
  }
]);

