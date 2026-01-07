import React, { useState } from 'react';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import ProductAnalytics from './ProductAnalytics';
import FinanceAnalytics from './FinanceAnalytics';
import CustomerAnalytics from './CustomerAnalytics';
import CombinedInsights from './CombinedInsights';
import FilterPanel from './components/FilterPanel';
import { BarChart3, DollarSign, Users, TrendingUp, ArrowLeft } from 'lucide-react';

const AnalyticsDashboard = () => {
  const [activeTab, setActiveTab] = useState('product');
  const [filters, setFilters] = useState({
    dateFilter: 'all',
    startDate: null,
    endDate: null,
    quoteStatus: 'all',
    productType: 'all',
    customer: 'all'
  });

  const handleFilterChange = (newFilters) => {
    setFilters(newFilters);
  };

  const handleBack = () => {
    window.location.href = '/';
  };

  return (
    <div className="w-full min-h-screen bg-gray-50 p-6">
      <div className="max-w-7xl mx-auto">
        {/* Header with Back Button */}
        <div className="mb-6 flex items-center justify-between">
          <div>
            <div className="flex items-center gap-4">
              <Button 
                onClick={handleBack}
                variant="outline"
                className="flex items-center gap-2"
              >
                <ArrowLeft className="w-4 h-4" />
                Back
              </Button>
              <h1 className="text-3xl font-bold text-gray-900">Analytics Dashboard</h1>
            </div>
            <p className="text-gray-600 mt-2">
              Comprehensive insights into products, finance, customers, and business trends
            </p>
          </div>
        </div>

        {/* Global Filter Panel */}
        <Card className="mb-6">
          <FilterPanel filters={filters} onFilterChange={handleFilterChange} />
        </Card>

        {/* Tabs */}
        <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
          <TabsList className="grid w-full grid-cols-4 mb-6">
            <TabsTrigger value="product" className="flex items-center gap-2">
              <BarChart3 className="w-4 h-4" />
              <span>Product View</span>
            </TabsTrigger>
            <TabsTrigger value="finance" className="flex items-center gap-2">
              <DollarSign className="w-4 h-4" />
              <span>Finance View</span>
            </TabsTrigger>
            <TabsTrigger value="customer" className="flex items-center gap-2">
              <Users className="w-4 h-4" />
              <span>Customer View</span>
            </TabsTrigger>
            <TabsTrigger value="insights" className="flex items-center gap-2">
              <TrendingUp className="w-4 h-4" />
              <span>Combined Insights</span>
            </TabsTrigger>
          </TabsList>

          <TabsContent value="product">
            <ProductAnalytics filters={filters} key={`product-${JSON.stringify(filters)}`} />
          </TabsContent>

          <TabsContent value="finance">
            <FinanceAnalytics filters={filters} key={`finance-${JSON.stringify(filters)}`} />
          </TabsContent>

          <TabsContent value="customer">
            <CustomerAnalytics filters={filters} key={`customer-${JSON.stringify(filters)}`} />
          </TabsContent>

          <TabsContent value="insights">
            <CombinedInsights filters={filters} key={`insights-${JSON.stringify(filters)}`} />
          </TabsContent>
        </Tabs>
      </div>
    </div>
  );
};

export default AnalyticsDashboard;






















// import React, { useState } from 'react';
// import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
// import { Card } from '@/components/ui/card';
// import ProductAnalytics from './ProductAnalytics';
// import FinanceAnalytics from './FinanceAnalytics';
// import CustomerAnalytics from './CustomerAnalytics';
// import CombinedInsights from './CombinedInsights';
// import FilterPanel from './components/FilterPanel';
// import { BarChart3, DollarSign, Users, TrendingUp } from 'lucide-react';

// const AnalyticsDashboard = () => {
//   const [activeTab, setActiveTab] = useState('product');
//   const [filters, setFilters] = useState({
//     dateFilter: 'all',
//     startDate: null,
//     endDate: null,
//     quoteStatus: 'all',
//     productType: 'all',
//     customer: 'all'
//   });

//   const handleFilterChange = (newFilters) => {
//     setFilters(newFilters);
//   };

//   return (
//     <div className="w-full min-h-screen bg-gray-50 p-6">
//       <div className="max-w-7xl mx-auto">
//         {/* Header */}
//         <div className="mb-6">
//           <h1 className="text-3xl font-bold text-gray-900">Analytics Dashboard</h1>
//           <p className="text-gray-600 mt-2">
//             Comprehensive insights into products, finance, customers, and business trends
//           </p>
//         </div>

//         {/* Global Filter Panel */}
//         <Card className="mb-6">
//           <FilterPanel filters={filters} onFilterChange={handleFilterChange} />
//         </Card>

//         {/* Tabs */}
//         <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
//           <TabsList className="grid w-full grid-cols-4 mb-6">
//             <TabsTrigger value="product" className="flex items-center gap-2">
//               <BarChart3 className="w-4 h-4" />
//               <span>Product View</span>
//             </TabsTrigger>
//             <TabsTrigger value="finance" className="flex items-center gap-2">
//               <DollarSign className="w-4 h-4" />
//               <span>Finance View</span>
//             </TabsTrigger>
//             <TabsTrigger value="customer" className="flex items-center gap-2">
//               <Users className="w-4 h-4" />
//               <span>Customer View</span>
//             </TabsTrigger>
//             <TabsTrigger value="insights" className="flex items-center gap-2">
//               <TrendingUp className="w-4 h-4" />
//               <span>Combined Insights</span>
//             </TabsTrigger>
//           </TabsList>

//           <TabsContent value="product">
//             <ProductAnalytics filters={filters} />
//           </TabsContent>

//           <TabsContent value="finance">
//             <FinanceAnalytics filters={filters} />
//           </TabsContent>

//           <TabsContent value="customer">
//             <CustomerAnalytics filters={filters} />
//           </TabsContent>

//           <TabsContent value="insights">
//             <CombinedInsights filters={filters} />
//           </TabsContent>
//         </Tabs>
//       </div>
//     </div>
//   );
// };

// export default AnalyticsDashboard;