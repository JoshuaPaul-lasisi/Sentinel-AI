"use client";

import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";
import { SectionHeader } from "./SectionHeader";

const data = [
  { time: "09:00", risk: 12, transactions: 45 },
  { time: "10:00", risk: 18, transactions: 67 },
  { time: "11:00", risk: 25, transactions: 89 },
  { time: "12:00", risk: 32, transactions: 112 },
  { time: "13:00", risk: 28, transactions: 98 },
  { time: "14:00", risk: 35, transactions: 134 },
  { time: "15:00", risk: 22, transactions: 76 },
];

export default function RiskChart() {
  return (
    <div className="bg-white p-6 rounded-xl shadow-md">
      <SectionHeader label="Risk Score Trends" />
      <div className="h-80">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={data}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="time" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Line
              type="monotone"
              dataKey="risk"
              stroke="#ef4444"
              strokeWidth={2}
              name="Risk Score"
            />
            <Line
              type="monotone"
              dataKey="transactions"
              stroke="#3b82f6"
              strokeWidth={2}
              name="Transactions"
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
