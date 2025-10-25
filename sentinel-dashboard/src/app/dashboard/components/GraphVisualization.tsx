'use client';

import { SectionHeader } from "./SectionHeader";

export default function GraphVisualization() {
  return (
    <div className="bg-white p-6 rounded-xl shadow-md">
        <SectionHeader 
        label="Money Mule Network Detection" />
      <div className="h-96 bg-linear-to-br from-blue-50 to-indigo-100 rounded-lg flex items-center justify-center">
        <div className="text-center">
          <div className="relative mx-auto w-64 h-48">
            {/* Simplified graph visualization */}
            <div className="absolute top-0 left-1/2 transform -translate-x-1/2 w-12 h-12 bg-red-500 rounded-full flex items-center justify-center text-white font-bold">
              A
            </div>
            <div className="absolute top-1/3 left-4 w-12 h-12 bg-yellow-500 rounded-full flex items-center justify-center text-white font-bold">
              B
            </div>
            <div className="absolute top-1/3 right-4 w-12 h-12 bg-yellow-500 rounded-full flex items-center justify-center text-white font-bold">
              C
            </div>
            <div className="absolute bottom-0 left-1/2 transform -translate-x-1/2 w-12 h-12 bg-green-500 rounded-full flex items-center justify-center text-white font-bold">
              D
            </div>
            
            {/* Connections */}
            <div className="absolute top-12 left-1/2 w-0.5 h-16 bg-gray-400 transform -translate-x-1/2"></div>
            <div className="absolute top-1/3 left-16 w-16 h-0.5 bg-gray-400"></div>
            <div className="absolute top-1/3 right-16 w-16 h-0.5 bg-gray-400"></div>
            <div className="absolute top-2/3 left-1/2 w-0.5 h-16 bg-gray-400 transform -translate-x-1/2"></div>
          </div>
          <p className="mt-4 text-gray-600">Real-time graph intelligence detecting circular transaction flows</p>
        </div>
      </div>
    </div>
  );
}