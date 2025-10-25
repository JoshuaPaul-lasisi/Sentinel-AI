'use client';

import { SectionHeader } from "./SectionHeader";

const features = [
  { name: 'BVN Age (2 hours)', contribution: 0.45, value: '2h' },
  { name: 'Transaction Amount', contribution: 0.28, value: '₦150,000' },
  { name: 'Device Mismatch', contribution: 0.15, value: 'Yes' },
  { name: 'Location Anomaly', contribution: 0.08, value: 'High' },
  { name: 'Time of Day', contribution: 0.04, value: 'Normal' },
];

export default function SHAPExplanation() {
  return (
    <div className="bg-white p-6 rounded-xl shadow-md">
        <SectionHeader
        label="AI Explanation - Why this was flagged"
        />
      <div className="space-y-3">
        {features.map((feature, index) => (
          <div key={index} className="flex items-center justify-between">
            <div className="flex-1">
              <div className="flex justify-between text-sm mb-1">
                <span className="font-medium text-gray-700">{feature.name}</span>
                <span className="text-gray-500">{feature.value}</span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div
                  className="bg-blue-600 h-2 rounded-full"
                  style={{ width: `${feature.contribution * 100}%` }}
                ></div>
              </div>
            </div>
            <div className="ml-4 text-sm font-medium text-gray-900 w-12 text-right">
              {Math.round(feature.contribution * 100)}%
            </div>
          </div>
        ))}
      </div>
      <div className="mt-4 p-4 bg-blue-50 rounded-lg">
        <p className="text-sm text-blue-800">
          <strong>Explanation:</strong> This transaction shows strong signs of BVN enrollment attack - 
          occurring just 2 hours after BVN registration with unusually high amount.
        </p>
      </div>
    </div>
  );
}