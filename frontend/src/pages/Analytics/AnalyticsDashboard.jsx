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
    <div style={styles.container}>
      <div style={styles.innerContainer}>
        {/* Header with Back Button */}
        <div style={styles.header}>
          <div>
            <div style={styles.headerTop}>
              <Button 
                onClick={handleBack}
                variant="outline"
                style={styles.backButton}
              >
                <ArrowLeft className="w-4 h-4" style={styles.backIcon} />
                Back
              </Button>
              <h1 style={styles.title}>Analytics Dashboard</h1>
            </div>
            <p style={styles.subtitle}>
              Comprehensive insights into products, finance, customers, and business trends
            </p>
          </div>
        </div>

        {/* Global Filter Panel - Enhanced styling */}
        <Card style={styles.filterCard}>
          <div style={styles.filterCardInner}>
            <FilterPanel filters={filters} onFilterChange={handleFilterChange} />
          </div>
        </Card>

        {/* Tabs - Enhanced styling */}
        <div style={styles.tabsContainer}>
          <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
            <div style={styles.tabsListWrapper}>
              <TabsList className="grid w-full grid-cols-4" style={styles.tabsList}>
                <TabsTrigger value="product" className="flex items-center gap-2" style={styles.tabTrigger}>
                  <BarChart3 className="w-4 h-4" />
                  <span>Product View</span>
                </TabsTrigger>
                <TabsTrigger value="finance" className="flex items-center gap-2" style={styles.tabTrigger}>
                  <DollarSign className="w-4 h-4" />
                  <span>Finance View</span>
                </TabsTrigger>
                <TabsTrigger value="customer" className="flex items-center gap-2" style={styles.tabTrigger}>
                  <Users className="w-4 h-4" />
                  <span>Customer View</span>
                </TabsTrigger>
                <TabsTrigger value="insights" className="flex items-center gap-2" style={styles.tabTrigger}>
                  <TrendingUp className="w-4 h-4" />
                  <span>Combined Insights</span>
                </TabsTrigger>
              </TabsList>
            </div>

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
    </div>
  );
};

const styles = {
  container: {
    width: '100%',
    minHeight: '100vh',
    backgroundColor: '#f3f4f6',
    padding: '20px',
  },
  innerContainer: {
    maxWidth: '1600px',
    margin: '0 auto',
  },
  header: {
    marginBottom: '24px',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'space-between',
  },
  headerTop: {
    display: 'flex',
    alignItems: 'center',
    gap: '16px',
  },
  backButton: {
    display: 'flex',
    alignItems: 'center',
    gap: '8px',
    padding: '10px 16px',
    fontSize: '14px',
    fontWeight: '500',
  },
  backIcon: {
    marginRight: '4px',
  },
  title: {
    fontSize: '32px',
    fontWeight: 'bold',
    color: '#111827',
    margin: 0,
  },
  subtitle: {
    color: '#6b7280',
    marginTop: '8px',
    fontSize: '15px',
  },
  filterCard: {
    marginBottom: '24px',
    boxShadow: '0 2px 6px rgba(0,0,0,0.08)',
    borderRadius: '12px',
    border: '1px solid #e5e7eb',
    backgroundColor: '#ffffff',
  },
  filterCardInner: {
    padding: '20px',
    backgroundColor: '#f9fafb',
    borderRadius: '11px',
  },
  tabsContainer: {
    backgroundColor: '#ffffff',
    borderRadius: '12px',
    padding: '8px',
    boxShadow: '0 2px 6px rgba(0,0,0,0.06)',
  },
  tabsListWrapper: {
    marginBottom: '20px',
    padding: '4px',
    backgroundColor: '#f9fafb',
    borderRadius: '10px',
  },
  tabsList: {
    backgroundColor: 'transparent',
    padding: '4px',
  },
  tabTrigger: {
    fontSize: '15px',
    fontWeight: '500',
    padding: '12px 16px',
  },
};

export default AnalyticsDashboard;










// import React, { useState } from 'react';
// import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
// import { Card } from '@/components/ui/card';
// import { Button } from '@/components/ui/button';
// import ProductAnalytics from './ProductAnalytics';
// import FinanceAnalytics from './FinanceAnalytics';
// import CustomerAnalytics from './CustomerAnalytics';
// import CombinedInsights from './CombinedInsights';
// import FilterPanel from './components/FilterPanel';
// import { BarChart3, DollarSign, Users, TrendingUp, ArrowLeft } from 'lucide-react';

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

//   const handleBack = () => {
//     window.location.href = '/';
//   };

//   return (
//     <div className="w-full min-h-screen bg-gray-50 p-6">
//       <div className="max-w-7xl mx-auto">
//         {/* Header with Back Button */}
//         <div className="mb-6 flex items-center justify-between">
//           <div>
//             <div className="flex items-center gap-4">
//               <Button 
//                 onClick={handleBack}
//                 variant="outline"
//                 className="flex items-center gap-2"
//               >
//                 <ArrowLeft className="w-4 h-4" />
//                 Back
//               </Button>
//               <h1 className="text-3xl font-bold text-gray-900">Analytics Dashboard</h1>
//             </div>
//             <p className="text-gray-600 mt-2">
//               Comprehensive insights into products, finance, customers, and business trends
//             </p>
//           </div>
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
//             <ProductAnalytics filters={filters} key={`product-${JSON.stringify(filters)}`} />
//           </TabsContent>

//           <TabsContent value="finance">
//             <FinanceAnalytics filters={filters} key={`finance-${JSON.stringify(filters)}`} />
//           </TabsContent>

//           <TabsContent value="customer">
//             <CustomerAnalytics filters={filters} key={`customer-${JSON.stringify(filters)}`} />
//           </TabsContent>

//           <TabsContent value="insights">
//             <CombinedInsights filters={filters} key={`insights-${JSON.stringify(filters)}`} />
//           </TabsContent>
//         </Tabs>
//       </div>
//     </div>
//   );
// };

// export default AnalyticsDashboard;
