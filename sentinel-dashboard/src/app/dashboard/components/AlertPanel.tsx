import { fraudPatterns } from '@lib/data';
import { SectionHeader } from './SectionHeader';

export default function AlertPanel() {
  return (
    <div className="bg-white p-6 rounded-xl shadow-md">
      <SectionHeader 
      label='Active Fraud Patterns'/>

      <div className="space-y-4">
        {fraudPatterns.map((pattern, index) => (
          <div key={index} className="border-l-4 border-red-500 pl-4 py-2">
            <div className="flex justify-between items-start">
              <div>
                <h4 className="font-semibold text-gray-900">{pattern.type}</h4>
                <p className="text-sm text-gray-600 mt-1">{pattern.description}</p>
                <p className="text-xs text-gray-500 mt-1">Detection: {pattern.detection}</p>
              </div>
              <span className="bg-red-100 text-red-800 text-xs font-medium px-2 py-1 rounded">
                {pattern.amount}
              </span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}