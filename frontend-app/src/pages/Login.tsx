import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Loader2 } from "lucide-react";

import { useAuth } from "../context/AuthProvider";
import { Button } from "../components/ui/Button";

export const LoginPage = () => {
  const { login } = useAuth();
  const navigate = useNavigate();
  const [form, setForm] = useState({ email: "", password: "" });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setLoading(true);
    setError(null);
    try {
      await login(form);
      navigate("/");
    } catch (err) {
      setError("Identifiants invalides");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex min-h-screen items-center justify-center bg-gradient-to-br from-[#f9f5eb] via-[#fffdf7] to-[#f4ead5] px-4 py-12">
      <div className="w-full max-w-md rounded-2xl border border-amber-100/60 bg-white/90 p-10 text-slate-700 shadow-glow-lg backdrop-blur-xl animate-scale-in">
        <div className="mb-6">
          <h1 className="mb-2 text-3xl font-bold gradient-text">Connexion EcoTrack</h1>
          <p className="text-sm font-medium text-slate-500">
            Accédez au tableau de bord environnemental
          </p>
        </div>
        <form className="space-y-5" onSubmit={handleSubmit}>
          <div className="animate-slide-up" style={{ animationDelay: "100ms" }}>
            <label className="text-xs font-semibold uppercase tracking-wide text-slate-600 mb-2 block">
              Email
            </label>
            <input
              type="email"
              className="form-field"
              value={form.email}
              onChange={(e) => setForm((prev) => ({ ...prev, email: e.target.value }))}
              required
            />
          </div>
          <div className="animate-slide-up" style={{ animationDelay: "200ms" }}>
            <label className="text-xs font-semibold uppercase tracking-wide text-slate-600 mb-2 block">
              Mot de passe
            </label>
            <input
              type="password"
              className="form-field"
              value={form.password}
              onChange={(e) => setForm((prev) => ({ ...prev, password: e.target.value }))}
              required
            />
          </div>
          {error && (
            <div className="animate-slide-up rounded-lg bg-rose-50/80 border border-rose-200/60 p-3">
              <p className="text-sm font-medium text-rose-600">{error}</p>
            </div>
          )}
          <div className="animate-slide-up" style={{ animationDelay: "300ms" }}>
            <Button
              type="submit"
              className="w-full justify-center mt-2"
              disabled={loading}
            >
              {loading ? (
                <>
                  <Loader2 className="mr-2 animate-spin" size={16} />
                  Connexion en cours
                </>
              ) : (
                "Se connecter"
              )}
            </Button>
          </div>
        </form>
      </div>
    </div>
  );
};

