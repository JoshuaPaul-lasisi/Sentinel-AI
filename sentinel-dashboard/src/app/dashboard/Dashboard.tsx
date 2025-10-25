import Header from './components/Header';
import StatsCards from './components/StatsCards';
import RiskChart from './components/RiskChart';
import TransactionTable from './components/TransactionTable';
import GraphVisualization from './components/GraphVisualization';
import SHAPExplanation from './components/SHAPExplanation';
import AlertPanel from './components/AlertPanel';

export default function Dashboard() {
  return (
    <div className="min-h-screen bg-gray-50 font-nunito">
      <Header />
      
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Stats Overview */}
        <StatsCards />
        
        {/* Main Dashboard Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 mb-8">
          {/* Left Column */}
          <div className="lg:col-span-2 space-y-8">
            <RiskChart />
            <TransactionTable />
          </div>
          
          {/* Right Column */}
          <div className="space-y-8">
            <AlertPanel />
            <SHAPExplanation />
            {/* <GraphVisualization /> */}
          </div>
        </div>

        {/* Key Metrics */}
        <div className="bg-white rounded-md shadow-lg p-6 mb-8">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Business Impact</h3>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-center">
            <div>
              <div className="text-2xl font-bold text-blue-600">2,403%</div>
              <div className="text-sm text-gray-500">ROI</div>
            </div>
            <div>
              <div className="text-2xl font-bold text-green-600">₦52B</div>
              <div className="text-sm text-gray-500">Problem Size</div>
            </div>
            <div>
              <div className="text-2xl font-bold text-purple-600">196%</div>
              <div className="text-sm text-gray-500">YoY Increase</div>
            </div>
            <div>
              <div className="text-2xl font-bold text-orange-600">₦1.5-2.2B</div>
              <div className="text-sm text-gray-500">Annual Savings</div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}