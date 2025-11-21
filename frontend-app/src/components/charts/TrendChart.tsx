import {
  Area,
  AreaChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis
} from "recharts";

type TrendChartProps = {
  data: { bucket: string; value: number }[];
  color?: string;
};

export const TrendChart = ({ data, color = "#0A84FF" }: TrendChartProps) => (
  <ResponsiveContainer width="100%" height={240}>
    <AreaChart data={data}>
      <defs>
        <linearGradient id="trend" x1="0" y1="0" x2="0" y2="1">
          <stop offset="5%" stopColor={color} stopOpacity={0.7} />
          <stop offset="95%" stopColor={color} stopOpacity={0} />
        </linearGradient>
      </defs>
      <XAxis dataKey="bucket" stroke="#94a3b8" />
      <YAxis stroke="#94a3b8" />
      <Tooltip
        contentStyle={{ background: "#0f172a", border: "1px solid #1e293b" }}
      />
      <Area
        type="monotone"
        dataKey="value"
        stroke={color}
        fillOpacity={1}
        fill="url(#trend)"
      />
    </AreaChart>
  </ResponsiveContainer>
);

