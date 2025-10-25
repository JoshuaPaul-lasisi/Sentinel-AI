import { statsData } from "@lib/data";
import { SectionHeader } from "./SectionHeader";

export default function StatsCards() {
  return (
    <div className="bg-white rounded-xl shadow-md p-6 mb-8">
      <SectionHeader label="Statistics" />

      <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8 font-nunito">
        <StatCard
          title="Total Transactions"
          value={statsData.totalTransactions.toLocaleString()}
          borderColor="border-blue-500"
        />
        <StatCard
          title="Fraud Detected"
          value={statsData.fraudDetected}
          borderColor="border-red-500"
        />
        <StatCard
          title="Money Saved"
          value={statsData.moneySaved}
          borderColor="border-green-500"
        />
        <StatCard
          title="Avg Response Time"
          value={statsData.avgResponseTime}
          borderColor="border-purple-500"
        />
      </div>
    </div>
  );
}

const StatCard = ({
  title,
  value,
  borderColor,
}: {
  title: string;
  value: string | number;
  borderColor: string;
}) => {
  return (
    <div
      className={`bg-white p-6 font-nunito rounded-md shadow-sm border-l-2 ${borderColor}`}
    >
      <h3 className="text-sm font-medium text mb-2 text-gray-500 tracking-wider">
        {title}
      </h3>
      <p className="text-2xl font-bold text-zinc-800 tracking-wide">{value}</p>
    </div>
  );
};
