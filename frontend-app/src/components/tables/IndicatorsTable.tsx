import { format } from "date-fns";
import { fr } from "date-fns/locale";

import type { Indicator } from "../../types";

type Props = {
  data: Indicator[];
};

export const IndicatorsTable = ({ data }: Props) => (
  <div className="overflow-hidden rounded-xl border border-amber-100/60 bg-white/90 shadow-soft">
    <table className="min-w-full divide-y divide-amber-50/60 text-left">
      <thead className="bg-gradient-to-r from-amber-50/90 to-white/90 text-xs font-bold uppercase tracking-wider text-slate-600">
        <tr>
          <th className="px-5 py-4">Type</th>
          <th className="px-5 py-4">Valeur</th>
          <th className="px-5 py-4">Zone</th>
          <th className="px-5 py-4">Source</th>
          <th className="px-5 py-4">Horodatage</th>
        </tr>
      </thead>
      <tbody className="divide-y divide-amber-50/40 bg-white/50 text-sm">
        {data.map((indicator, index) => (
          <tr 
            key={indicator.id} 
            className="transition-all duration-200 hover:bg-gradient-to-r hover:from-amber-50/80 hover:to-white/80 hover:shadow-sm animate-slide-up"
            style={{ animationDelay: `${index * 30}ms` }}
          >
            <td className="px-5 py-3.5 font-bold text-slate-800">{indicator.type}</td>
            <td className="px-5 py-3.5">
              <span className="font-bold text-brand-dark text-base">
                {indicator.value.toFixed(2)} <span className="text-xs font-semibold text-slate-500">{indicator.unit}</span>
              </span>
            </td>
            <td className="px-5 py-3.5 font-medium text-slate-700">{indicator.zone?.name ?? `#${indicator.zone_id}`}</td>
            <td className="px-5 py-3.5 font-medium text-slate-600">{indicator.source?.name ?? "N/A"}</td>
            <td className="px-5 py-3.5 text-slate-500 font-medium">
              {format(new Date(indicator.timestamp), "dd MMM yyyy HH:mm", { locale: fr })}
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  </div>
);

