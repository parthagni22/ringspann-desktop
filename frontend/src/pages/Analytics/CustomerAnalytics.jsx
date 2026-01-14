import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import KPICard from './components/KPICard';
import CustomerFilterPanel from './components/CustomerFilterPanel';
import { useCustomerAnalytics, exportAnalyticsData } from './hooks/useAnalyticsData.js';
import {
  BarChart, Bar, PieChart, Pie, Cell,
  XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer
} from 'recharts';
import { Download, Users, DollarSign, TrendingUp, UserCheck, UserPlus } from 'lucide-react';
import { Loader2 } from 'lucide-react';

const COLORS = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6'];

const CustomerAnalytics = ({ filters, onFilterChange }) => {
  const { data, loading, error } = useCustomerAnalytics(filters);

  const handleExport = async () => {
    const result = await exportAnalyticsData('customer', 'csv', filters);
    if (result.success) {
      alert(`Data exported successfully!\n\nFile: ${result.filename}\nLocation: data/exports/\n\n${result.message}`);
    } else {
      alert(`Export failed: ${result.error}`);
    }
  };

  if (loading) {
    return (
      <div style={styles.loadingContainer}>
        <Loader2 className="w-8 h-8 animate-spin text-blue-600" />
        <span style={styles.loadingText}>Loading customer analytics...</span>
      </div>
    );
  }

  if (error) {
    return (
      <div style={styles.errorContainer}>
        <div style={styles.errorContent}>
          <p style={styles.errorText}>{error}</p>
          <Button onClick={() => window.location.reload()} style={styles.retryButton}>
            Retry
          </Button>
        </div>
      </div>
    );
  }

  if (!data) return null;

  const { 
    kpis, 
    top_customers_by_count, 
    top_customers_by_revenue, 
    customer_status_breakdown, 
    activity_timeline,
    new_vs_repeat 
  } = data;

  // Prepare new vs repeat data for pie chart
  const newVsRepeatData = [
    { name: 'New Customers', value: new_vs_repeat.new },
    { name: 'Repeat Customers', value: new_vs_repeat.repeat }
  ];

  return (
    <div style={styles.container}>
      {/* Tab-Specific Customer Filter Panel */}
      <CustomerFilterPanel filters={filters} onFilterChange={onFilterChange} />

      {/* Export Button */}
      <div style={styles.exportSection}>
        <Button
          variant="outline"
          onClick={handleExport}
          style={styles.exportButton}
        >
          <Download className="w-4 h-4" />
          <span style={styles.exportText}>Export CSV</span>
        </Button>
      </div>

      {/* KPI Cards */}
      <div style={styles.kpiGrid}>
        <KPICard
          label={kpis.total_customers.label}
          value={kpis.total_customers.value}
          changePercent={kpis.total_customers.change_percent}
          changeDirection={kpis.total_customers.change_direction}
          formatType={kpis.total_customers.format_type}
          icon={Users}
        />
        <KPICard
          label={kpis.total_revenue.label}
          value={kpis.total_revenue.value}
          changePercent={kpis.total_revenue.change_percent}
          changeDirection={kpis.total_revenue.change_direction}
          formatType={kpis.total_revenue.format_type}
          icon={DollarSign}
        />
        <KPICard
          label={kpis.avg_revenue_per_customer.label}
          value={kpis.avg_revenue_per_customer.value}
          changePercent={kpis.avg_revenue_per_customer.change_percent}
          changeDirection={kpis.avg_revenue_per_customer.change_direction}
          formatType={kpis.avg_revenue_per_customer.format_type}
          icon={TrendingUp}
        />
        <KPICard
          label={kpis.new_customers.label}
          value={kpis.new_customers.value}
          formatType={kpis.new_customers.format_type}
          icon={UserPlus}
        />
        <KPICard
          label={kpis.repeat_customers.label}
          value={kpis.repeat_customers.value}
          formatType={kpis.repeat_customers.format_type}
          icon={UserCheck}
        />
      </div>

      {/* Charts Row 1 */}
      <div style={styles.chartsRow}>
        {/* Top Customers by Quote Count - with horizontal scroll */}
        <Card style={styles.chartCard}>
          <CardHeader style={styles.cardHeader}>
            <CardTitle style={styles.cardTitle}>Top Customers by Quote Count</CardTitle>
          </CardHeader>
          <CardContent style={styles.cardContent}>
            <div style={styles.chartScrollWrapper}>
              <div style={{ minWidth: Math.max(800, top_customers_by_count.slice(0, 10).length * 80) }}>
                <ResponsiveContainer width="100%" height={400}>
                  <BarChart data={top_customers_by_count.slice(0, 10)}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
                    <XAxis 
                      dataKey="customer_name" 
                      angle={-45}
                      textAnchor="end"
                      height={140}
                      interval={0}
                      tick={{ fontSize: 12, fill: '#374151' }}
                    />
                    <YAxis tick={{ fontSize: 13, fill: '#374151' }} />
                    <Tooltip contentStyle={{ fontSize: '14px' }} />
                    <Legend wrapperStyle={{ fontSize: '14px', paddingTop: '10px' }} />
                    <Bar dataKey="quote_count" fill="#f59e0b" name="Quotes" radius={[6, 6, 0, 0]} />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Top Customers by Revenue - with horizontal scroll */}
        <Card style={styles.chartCard}>
          <CardHeader style={styles.cardHeader}>
            <CardTitle style={styles.cardTitle}>Top Customers by Revenue</CardTitle>
          </CardHeader>
          <CardContent style={styles.cardContent}>
            <div style={styles.chartScrollWrapper}>
              <div style={{ minWidth: Math.max(800, top_customers_by_revenue.slice(0, 10).length * 80) }}>
                <ResponsiveContainer width="100%" height={400}>
                  <BarChart data={top_customers_by_revenue.slice(0, 10)}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
                    <XAxis 
                      dataKey="customer_name" 
                      angle={-45}
                      textAnchor="end"
                      height={140}
                      interval={0}
                      tick={{ fontSize: 12, fill: '#374151' }}
                    />
                    <YAxis tick={{ fontSize: 13, fill: '#374151' }} />
                    <Tooltip formatter={(value) => `$${value.toLocaleString()}`} contentStyle={{ fontSize: '14px' }} />
                    <Legend wrapperStyle={{ fontSize: '14px', paddingTop: '10px' }} />
                    <Bar dataKey="revenue" fill="#10b981" name="Revenue" radius={[6, 6, 0, 0]} />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Charts Row 2 */}
      <div style={styles.chartsRow}>
        {/* Customer Status Breakdown - with horizontal scroll */}
        <Card style={styles.chartCard}>
          <CardHeader style={styles.cardHeader}>
            <CardTitle style={styles.cardTitle}>Customer Quote Status Breakdown</CardTitle>
          </CardHeader>
          <CardContent style={styles.cardContent}>
            <div style={styles.chartScrollWrapper}>
              <div style={{ minWidth: Math.max(800, customer_status_breakdown.slice(0, 10).length * 80) }}>
                <ResponsiveContainer width="100%" height={400}>
                  <BarChart data={customer_status_breakdown.slice(0, 10)}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
                    <XAxis 
                      dataKey="customer_name"
                      angle={-45}
                      textAnchor="end"
                      height={140}
                      interval={0}
                      tick={{ fontSize: 12, fill: '#374151' }}
                    />
                    <YAxis tick={{ fontSize: 13, fill: '#374151' }} />
                    <Tooltip contentStyle={{ fontSize: '14px' }} />
                    <Legend wrapperStyle={{ fontSize: '13px', paddingTop: '10px' }} />
                    <Bar dataKey="Budgetary" stackId="a" fill="#fbbf24" name="Budgetary" />
                    <Bar dataKey="Active" stackId="a" fill="#3b82f6" name="Active" />
                    <Bar dataKey="Won" stackId="a" fill="#10b981" name="Won" />
                    <Bar dataKey="Lost" stackId="a" fill="#ef4444" name="Lost" radius={[6, 6, 0, 0]} />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* New vs Repeat Customers */}
        <Card style={styles.chartCard}>
          <CardHeader style={styles.cardHeader}>
            <CardTitle style={styles.cardTitle}>New vs Repeat Customers</CardTitle>
          </CardHeader>
          <CardContent style={styles.cardContent}>
            <ResponsiveContainer width="100%" height={400}>
              <PieChart>
                <Pie
                  data={newVsRepeatData}
                  dataKey="value"
                  nameKey="name"
                  cx="50%"
                  cy="45%"
                  outerRadius={120}
                  label={(entry) => `${entry.value}`}
                  labelLine={true}
                >
                  {newVsRepeatData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip contentStyle={{ fontSize: '14px' }} />
                <Legend wrapperStyle={{ fontSize: '14px' }} />
              </PieChart>
            </ResponsiveContainer>
            <div style={styles.pieChartInfo}>
              <p style={styles.pieChartText}>
                Total: {new_vs_repeat.total} customers
              </p>
              <p style={styles.pieChartText}>
                Repeat Rate: {((new_vs_repeat.repeat / new_vs_repeat.total) * 100).toFixed(1)}%
              </p>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Data Tables */}
      <div style={styles.tableSection}>
        {/* Top Customers Detail Table */}
        <Card style={styles.tableCard}>
          <CardHeader style={styles.cardHeader}>
            <CardTitle style={styles.cardTitle}>Top Customer Performance</CardTitle>
          </CardHeader>
          <CardContent style={styles.cardContent}>
            <div style={styles.tableWrapper}>
              <table style={styles.table}>
                <thead>
                  <tr style={styles.tableHeaderRow}>
                    <th style={styles.tableHeader}>Customer Name</th>
                    <th style={{ ...styles.tableHeader, textAlign: 'right' }}>Quotes</th>
                    <th style={{ ...styles.tableHeader, textAlign: 'right' }}>Total Revenue</th>
                    <th style={{ ...styles.tableHeader, textAlign: 'right' }}>Avg Deal Size</th>
                    <th style={{ ...styles.tableHeader, textAlign: 'right' }}>Last Quote</th>
                  </tr>
                </thead>
                <tbody>
                  {top_customers_by_revenue.slice(0, 15).map((customer, index) => (
                    <tr key={index} style={styles.tableRow}>
                      <td style={styles.tableCell}>{customer.customer_name}</td>
                      <td style={{ ...styles.tableCell, textAlign: 'right' }}>{customer.quote_count}</td>
                      <td style={{ ...styles.tableCell, textAlign: 'right' }}>${customer.revenue.toLocaleString()}</td>
                      <td style={{ ...styles.tableCell, textAlign: 'right' }}>${customer.avg_deal_size.toLocaleString()}</td>
                      <td style={{ ...styles.tableCell, textAlign: 'right' }}>{customer.last_quote_date || 'N/A'}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </CardContent>
        </Card>

        {/* Recent Customer Activity */}
        <Card style={styles.tableCard}>
          <CardHeader style={styles.cardHeader}>
            <CardTitle style={styles.cardTitle}>Recent Customer Activity</CardTitle>
          </CardHeader>
          <CardContent style={styles.cardContent}>
            <div style={styles.tableWrapper}>
              <table style={styles.table}>
                <thead>
                  <tr style={styles.tableHeaderRow}>
                    <th style={styles.tableHeader}>Date</th>
                    <th style={styles.tableHeader}>Customer</th>
                    <th style={styles.tableHeader}>Quotation #</th>
                    <th style={styles.tableHeader}>Status</th>
                  </tr>
                </thead>
                <tbody>
                  {activity_timeline.slice(0, 20).map((activity, index) => (
                    <tr key={index} style={styles.tableRow}>
                      <td style={styles.tableCell}>{activity.date}</td>
                      <td style={styles.tableCell}>{activity.customer_name}</td>
                      <td style={styles.tableCell}>{activity.quotation_number}</td>
                      <td style={styles.tableCell}>
                        <span style={{
                          ...styles.statusBadge,
                          ...(activity.status === 'Won' ? styles.statusWon :
                              activity.status === 'Lost' ? styles.statusLost :
                              activity.status === 'Active' ? styles.statusActive :
                              styles.statusBudgetary)
                        }}>
                          {activity.status}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

const styles = {
  container: {
    width: '100%',
    maxHeight: 'calc(100vh - 280px)',
    overflowY: 'auto',
    overflowX: 'hidden',
    padding: '0 8px',
  },
  loadingContainer: {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    height: '400px',
    flexDirection: 'column',
    gap: '12px',
  },
  loadingText: {
    color: '#6b7280',
    fontSize: '14px',
  },
  errorContainer: {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    height: '400px',
  },
  errorContent: {
    textAlign: 'center',
  },
  errorText: {
    color: '#dc2626',
    fontWeight: '500',
    marginBottom: '16px',
  },
  retryButton: {
    marginTop: '16px',
  },
  exportSection: {
    display: 'flex',
    justifyContent: 'flex-end',
    gap: '10px',
    marginBottom: '20px',
  },
  exportButton: {
    display: 'flex',
    alignItems: 'center',
    gap: '8px',
    padding: '10px 18px',
    fontSize: '14px',
    fontWeight: '500',
    backgroundColor: '#ffffff',
    color: '#374151',
    border: '1px solid #d1d5db',
    borderRadius: '8px',
    cursor: 'pointer',
  },
  exportText: {
    marginLeft: '4px',
  },
  kpiGrid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))',
    gap: '18px',
    marginBottom: '28px',
  },
  chartsRow: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(600px, 1fr))',
    gap: '24px',
    marginBottom: '28px',
  },
  chartCard: {
    boxShadow: '0 2px 4px rgba(0,0,0,0.08)',
    borderRadius: '12px',
    border: '1px solid #e5e7eb',
  },
  cardHeader: {
    padding: '20px',
    borderBottom: '2px solid #f3f4f6',
  },
  cardTitle: {
    fontSize: '17px',
    fontWeight: '600',
    color: '#111827',
  },
  cardContent: {
    padding: '20px',
  },
  chartScrollWrapper: {
    overflowX: 'auto',
    overflowY: 'hidden',
  },
  pieChartInfo: {
    marginTop: '20px',
    textAlign: 'center',
  },
  pieChartText: {
    fontSize: '14px',
    color: '#6b7280',
    margin: '6px 0',
  },
  tableSection: {
    display: 'grid',
    gridTemplateColumns: '1fr',
    gap: '24px',
    marginBottom: '28px',
  },
  tableCard: {
    boxShadow: '0 2px 4px rgba(0,0,0,0.08)',
    borderRadius: '12px',
    border: '1px solid #e5e7eb',
  },
  tableWrapper: {
    overflowX: 'auto',
    maxHeight: '400px',
    overflowY: 'auto',
  },
  table: {
    width: '100%',
    borderCollapse: 'collapse',
    fontSize: '14px',
  },
  tableHeaderRow: {
    backgroundColor: '#f9fafb',
    position: 'sticky',
    top: 0,
    zIndex: 1,
  },
  tableHeader: {
    padding: '14px',
    textAlign: 'left',
    fontWeight: '600',
    color: '#374151',
    borderBottom: '2px solid #e5e7eb',
    fontSize: '14px',
  },
  tableRow: {
    borderBottom: '1px solid #e5e7eb',
  },
  tableCell: {
    padding: '14px',
    color: '#1f2937',
    fontSize: '14px',
  },
  statusBadge: {
    padding: '5px 10px',
    borderRadius: '14px',
    fontSize: '12px',
    fontWeight: '500',
  },
  statusWon: {
    backgroundColor: '#dcfce7',
    color: '#166534',
  },
  statusLost: {
    backgroundColor: '#fee2e2',
    color: '#991b1b',
  },
  statusActive: {
    backgroundColor: '#dbeafe',
    color: '#1e40af',
  },
  statusBudgetary: {
    backgroundColor: '#fef3c7',
    color: '#92400e',
  },
};

export default CustomerAnalytics;


























// import React from 'react';
// import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
// import { Button } from '@/components/ui/button';
// import KPICard from './components/KPICard';
// import { useCustomerAnalytics, exportAnalyticsData } from './hooks/useAnalyticsData.js';
// import {
//   BarChart, Bar, PieChart, Pie, Cell,
//   XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer
// } from 'recharts';
// import { Download, Users, DollarSign, TrendingUp, UserCheck, UserPlus } from 'lucide-react';
// import { Loader2 } from 'lucide-react';

// const COLORS = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6'];

// const CustomerAnalytics = ({ filters }) => {
//   const { data, loading, error } = useCustomerAnalytics(filters);

//   const handleExport = async (format) => {
//     const result = await exportAnalyticsData('customer', format, filters);
//     if (result.success) {
//       alert(`Data exported successfully as ${format.toUpperCase()}`);
//     } else {
//       alert(`Export failed: ${result.error}`);
//     }
//   };

//   if (loading) {
//     return (
//       <div style={styles.loadingContainer}>
//         <Loader2 className="w-8 h-8 animate-spin text-blue-600" />
//         <span style={styles.loadingText}>Loading customer analytics...</span>
//       </div>
//     );
//   }

//   if (error) {
//     return (
//       <div style={styles.errorContainer}>
//         <div style={styles.errorContent}>
//           <p style={styles.errorText}>{error}</p>
//           <Button onClick={() => window.location.reload()} style={styles.retryButton}>
//             Retry
//           </Button>
//         </div>
//       </div>
//     );
//   }

//   if (!data) return null;

//   const { 
//     kpis, 
//     top_customers_by_count, 
//     top_customers_by_revenue, 
//     customer_status_breakdown, 
//     activity_timeline,
//     new_vs_repeat 
//   } = data;

//   // Prepare new vs repeat data for pie chart
//   const newVsRepeatData = [
//     { name: 'New Customers', value: new_vs_repeat.new },
//     { name: 'Repeat Customers', value: new_vs_repeat.repeat }
//   ];

//   return (
//     <div style={styles.container}>
//       {/* Export Buttons */}
//       <div style={styles.exportSection}>
//         <Button
//           variant="outline"
//           onClick={() => handleExport('json')}
//           style={styles.exportButton}
//         >
//           <Download className="w-4 h-4" />
//           <span style={styles.exportText}>Export JSON</span>
//         </Button>
//         <Button
//           variant="outline"
//           onClick={() => handleExport('csv')}
//           style={styles.exportButton}
//         >
//           <Download className="w-4 h-4" />
//           <span style={styles.exportText}>Export CSV</span>
//         </Button>
//       </div>

//       {/* KPI Cards */}
//       <div style={styles.kpiGrid}>
//         <KPICard
//           label={kpis.total_customers.label}
//           value={kpis.total_customers.value}
//           changePercent={kpis.total_customers.change_percent}
//           changeDirection={kpis.total_customers.change_direction}
//           formatType={kpis.total_customers.format_type}
//           icon={Users}
//         />
//         <KPICard
//           label={kpis.total_revenue.label}
//           value={kpis.total_revenue.value}
//           changePercent={kpis.total_revenue.change_percent}
//           changeDirection={kpis.total_revenue.change_direction}
//           formatType={kpis.total_revenue.format_type}
//           icon={DollarSign}
//         />
//         <KPICard
//           label={kpis.avg_revenue_per_customer.label}
//           value={kpis.avg_revenue_per_customer.value}
//           changePercent={kpis.avg_revenue_per_customer.change_percent}
//           changeDirection={kpis.avg_revenue_per_customer.change_direction}
//           formatType={kpis.avg_revenue_per_customer.format_type}
//           icon={TrendingUp}
//         />
//         <KPICard
//           label={kpis.new_customers.label}
//           value={kpis.new_customers.value}
//           formatType={kpis.new_customers.format_type}
//           icon={UserPlus}
//         />
//         <KPICard
//           label={kpis.repeat_customers.label}
//           value={kpis.repeat_customers.value}
//           formatType={kpis.repeat_customers.format_type}
//           icon={UserCheck}
//         />
//       </div>

//       {/* Charts Row 1 */}
//       <div style={styles.chartsRow}>
//         {/* Top Customers by Quote Count - with horizontal scroll */}
//         <Card style={styles.chartCard}>
//           <CardHeader style={styles.cardHeader}>
//             <CardTitle style={styles.cardTitle}>Top Customers by Quote Count</CardTitle>
//           </CardHeader>
//           <CardContent style={styles.cardContent}>
//             <div style={styles.chartScrollWrapper}>
//               <div style={{ minWidth: Math.max(800, top_customers_by_count.slice(0, 10).length * 80) }}>
//                 <ResponsiveContainer width="100%" height={400}>
//                   <BarChart data={top_customers_by_count.slice(0, 10)}>
//                     <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
//                     <XAxis 
//                       dataKey="customer_name" 
//                       angle={-45}
//                       textAnchor="end"
//                       height={140}
//                       interval={0}
//                       tick={{ fontSize: 12, fill: '#374151' }}
//                     />
//                     <YAxis tick={{ fontSize: 13, fill: '#374151' }} />
//                     <Tooltip contentStyle={{ fontSize: '14px' }} />
//                     <Legend wrapperStyle={{ fontSize: '14px', paddingTop: '10px' }} />
//                     <Bar dataKey="quote_count" fill="#3b82f6" name="Quotes" radius={[6, 6, 0, 0]} />
//                   </BarChart>
//                 </ResponsiveContainer>
//               </div>
//             </div>
//           </CardContent>
//         </Card>

//         {/* Top Customers by Revenue - with horizontal scroll */}
//         <Card style={styles.chartCard}>
//           <CardHeader style={styles.cardHeader}>
//             <CardTitle style={styles.cardTitle}>Top Customers by Revenue</CardTitle>
//           </CardHeader>
//           <CardContent style={styles.cardContent}>
//             <div style={styles.chartScrollWrapper}>
//               <div style={{ minWidth: Math.max(800, top_customers_by_revenue.slice(0, 10).length * 80) }}>
//                 <ResponsiveContainer width="100%" height={400}>
//                   <BarChart data={top_customers_by_revenue.slice(0, 10)}>
//                     <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
//                     <XAxis 
//                       dataKey="customer_name" 
//                       angle={-45}
//                       textAnchor="end"
//                       height={140}
//                       interval={0}
//                       tick={{ fontSize: 12, fill: '#374151' }}
//                     />
//                     <YAxis tick={{ fontSize: 13, fill: '#374151' }} />
//                     <Tooltip formatter={(value) => `$${value.toLocaleString()}`} contentStyle={{ fontSize: '14px' }} />
//                     <Legend wrapperStyle={{ fontSize: '14px', paddingTop: '10px' }} />
//                     <Bar dataKey="revenue" fill="#10b981" name="Revenue" radius={[6, 6, 0, 0]} />
//                   </BarChart>
//                 </ResponsiveContainer>
//               </div>
//             </div>
//           </CardContent>
//         </Card>
//       </div>

//       {/* Charts Row 2 */}
//       <div style={styles.chartsRow}>
//         {/* Customer Status Breakdown - with horizontal scroll */}
//         <Card style={styles.chartCard}>
//           <CardHeader style={styles.cardHeader}>
//             <CardTitle style={styles.cardTitle}>Customer Quote Status Breakdown</CardTitle>
//           </CardHeader>
//           <CardContent style={styles.cardContent}>
//             <div style={styles.chartScrollWrapper}>
//               <div style={{ minWidth: Math.max(800, customer_status_breakdown.slice(0, 10).length * 80) }}>
//                 <ResponsiveContainer width="100%" height={400}>
//                   <BarChart data={customer_status_breakdown.slice(0, 10)}>
//                     <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
//                     <XAxis 
//                       dataKey="customer_name"
//                       angle={-45}
//                       textAnchor="end"
//                       height={140}
//                       interval={0}
//                       tick={{ fontSize: 12, fill: '#374151' }}
//                     />
//                     <YAxis tick={{ fontSize: 13, fill: '#374151' }} />
//                     <Tooltip contentStyle={{ fontSize: '14px' }} />
//                     <Legend wrapperStyle={{ fontSize: '13px', paddingTop: '10px' }} />
//                     <Bar dataKey="Budgetary" stackId="a" fill="#fbbf24" name="Budgetary" />
//                     <Bar dataKey="Active" stackId="a" fill="#3b82f6" name="Active" />
//                     <Bar dataKey="Won" stackId="a" fill="#10b981" name="Won" />
//                     <Bar dataKey="Lost" stackId="a" fill="#ef4444" name="Lost" radius={[6, 6, 0, 0]} />
//                   </BarChart>
//                 </ResponsiveContainer>
//               </div>
//             </div>
//           </CardContent>
//         </Card>

//         {/* New vs Repeat Customers */}
//         <Card style={styles.chartCard}>
//           <CardHeader style={styles.cardHeader}>
//             <CardTitle style={styles.cardTitle}>New vs Repeat Customers</CardTitle>
//           </CardHeader>
//           <CardContent style={styles.cardContent}>
//             <ResponsiveContainer width="100%" height={400}>
//               <PieChart>
//                 <Pie
//                   data={newVsRepeatData}
//                   dataKey="value"
//                   nameKey="name"
//                   cx="50%"
//                   cy="45%"
//                   outerRadius={120}
//                   label={(entry) => `${entry.value}`}
//                   labelLine={true}
//                 >
//                   {newVsRepeatData.map((entry, index) => (
//                     <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
//                   ))}
//                 </Pie>
//                 <Tooltip contentStyle={{ fontSize: '14px' }} />
//                 <Legend wrapperStyle={{ fontSize: '14px' }} />
//               </PieChart>
//             </ResponsiveContainer>
//             <div style={styles.pieChartInfo}>
//               <p style={styles.pieChartText}>
//                 Total: {new_vs_repeat.total} customers
//               </p>
//               <p style={styles.pieChartText}>
//                 Repeat Rate: {((new_vs_repeat.repeat / new_vs_repeat.total) * 100).toFixed(1)}%
//               </p>
//             </div>
//           </CardContent>
//         </Card>
//       </div>

//       {/* Data Tables */}
//       <div style={styles.tableSection}>
//         {/* Top Customers Detail Table */}
//         <Card style={styles.tableCard}>
//           <CardHeader style={styles.cardHeader}>
//             <CardTitle style={styles.cardTitle}>Top Customer Performance</CardTitle>
//           </CardHeader>
//           <CardContent style={styles.cardContent}>
//             <div style={styles.tableWrapper}>
//               <table style={styles.table}>
//                 <thead>
//                   <tr style={styles.tableHeaderRow}>
//                     <th style={styles.tableHeader}>Customer Name</th>
//                     <th style={{ ...styles.tableHeader, textAlign: 'right' }}>Quotes</th>
//                     <th style={{ ...styles.tableHeader, textAlign: 'right' }}>Total Revenue</th>
//                     <th style={{ ...styles.tableHeader, textAlign: 'right' }}>Avg Deal Size</th>
//                     <th style={{ ...styles.tableHeader, textAlign: 'right' }}>Last Quote</th>
//                   </tr>
//                 </thead>
//                 <tbody>
//                   {top_customers_by_revenue.slice(0, 15).map((customer, index) => (
//                     <tr key={index} style={styles.tableRow}>
//                       <td style={styles.tableCell}>{customer.customer_name}</td>
//                       <td style={{ ...styles.tableCell, textAlign: 'right' }}>{customer.quote_count}</td>
//                       <td style={{ ...styles.tableCell, textAlign: 'right' }}>${customer.revenue.toLocaleString()}</td>
//                       <td style={{ ...styles.tableCell, textAlign: 'right' }}>${customer.avg_deal_size.toLocaleString()}</td>
//                       <td style={{ ...styles.tableCell, textAlign: 'right' }}>{customer.last_quote_date || 'N/A'}</td>
//                     </tr>
//                   ))}
//                 </tbody>
//               </table>
//             </div>
//           </CardContent>
//         </Card>

//         {/* Recent Customer Activity */}
//         <Card style={styles.tableCard}>
//           <CardHeader style={styles.cardHeader}>
//             <CardTitle style={styles.cardTitle}>Recent Customer Activity</CardTitle>
//           </CardHeader>
//           <CardContent style={styles.cardContent}>
//             <div style={styles.tableWrapper}>
//               <table style={styles.table}>
//                 <thead>
//                   <tr style={styles.tableHeaderRow}>
//                     <th style={styles.tableHeader}>Date</th>
//                     <th style={styles.tableHeader}>Customer</th>
//                     <th style={styles.tableHeader}>Quotation #</th>
//                     <th style={styles.tableHeader}>Status</th>
//                   </tr>
//                 </thead>
//                 <tbody>
//                   {activity_timeline.slice(0, 20).map((activity, index) => (
//                     <tr key={index} style={styles.tableRow}>
//                       <td style={styles.tableCell}>{activity.date}</td>
//                       <td style={styles.tableCell}>{activity.customer_name}</td>
//                       <td style={styles.tableCell}>{activity.quotation_number}</td>
//                       <td style={styles.tableCell}>
//                         <span style={{
//                           ...styles.statusBadge,
//                           ...(activity.status === 'Won' ? styles.statusWon :
//                               activity.status === 'Lost' ? styles.statusLost :
//                               activity.status === 'Active' ? styles.statusActive :
//                               styles.statusBudgetary)
//                         }}>
//                           {activity.status}
//                         </span>
//                       </td>
//                     </tr>
//                   ))}
//                 </tbody>
//               </table>
//             </div>
//           </CardContent>
//         </Card>
//       </div>
//     </div>
//   );
// };

// const styles = {
//   container: {
//     width: '100%',
//     maxHeight: 'calc(100vh - 280px)',
//     overflowY: 'auto',
//     overflowX: 'hidden',
//     padding: '0 8px',
//   },
//   loadingContainer: {
//     display: 'flex',
//     alignItems: 'center',
//     justifyContent: 'center',
//     height: '400px',
//     flexDirection: 'column',
//     gap: '12px',
//   },
//   loadingText: {
//     color: '#6b7280',
//     fontSize: '14px',
//   },
//   errorContainer: {
//     display: 'flex',
//     alignItems: 'center',
//     justifyContent: 'center',
//     height: '400px',
//   },
//   errorContent: {
//     textAlign: 'center',
//   },
//   errorText: {
//     color: '#dc2626',
//     fontWeight: '500',
//     marginBottom: '16px',
//   },
//   retryButton: {
//     marginTop: '16px',
//   },
//   exportSection: {
//     display: 'flex',
//     justifyContent: 'flex-end',
//     gap: '10px',
//     marginBottom: '20px',
//   },
//   exportButton: {
//     display: 'flex',
//     alignItems: 'center',
//     gap: '8px',
//     padding: '10px 18px',
//     fontSize: '14px',
//   },
//   exportText: {
//     marginLeft: '4px',
//   },
//   kpiGrid: {
//     display: 'grid',
//     gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))',
//     gap: '18px',
//     marginBottom: '28px',
//   },
//   chartsRow: {
//     display: 'grid',
//     gridTemplateColumns: 'repeat(auto-fit, minmax(600px, 1fr))',
//     gap: '24px',
//     marginBottom: '28px',
//   },
//   chartCard: {
//     boxShadow: '0 2px 4px rgba(0,0,0,0.08)',
//     borderRadius: '10px',
//     border: '1px solid #e5e7eb',
//   },
//   cardHeader: {
//     padding: '20px',
//     borderBottom: '2px solid #e5e7eb',
//     backgroundColor: '#f9fafb',
//   },
//   cardTitle: {
//     fontSize: '17px',
//     fontWeight: '600',
//     color: '#111827',
//   },
//   cardContent: {
//     padding: '20px',
//   },
//   chartScrollWrapper: {
//     overflowX: 'auto',
//     overflowY: 'hidden',
//   },
//   pieChartInfo: {
//     marginTop: '20px',
//     textAlign: 'center',
//   },
//   pieChartText: {
//     fontSize: '14px',
//     color: '#6b7280',
//     margin: '6px 0',
//   },
//   tableSection: {
//     display: 'grid',
//     gridTemplateColumns: '1fr',
//     gap: '24px',
//     marginBottom: '28px',
//   },
//   tableCard: {
//     boxShadow: '0 2px 4px rgba(0,0,0,0.08)',
//     borderRadius: '10px',
//     border: '1px solid #e5e7eb',
//   },
//   tableWrapper: {
//     overflowX: 'auto',
//     maxHeight: '400px',
//     overflowY: 'auto',
//   },
//   table: {
//     width: '100%',
//     borderCollapse: 'collapse',
//     fontSize: '14px',
//   },
//   tableHeaderRow: {
//     backgroundColor: '#f9fafb',
//     position: 'sticky',
//     top: 0,
//     zIndex: 1,
//   },
//   tableHeader: {
//     padding: '14px',
//     textAlign: 'left',
//     fontWeight: '600',
//     color: '#374151',
//     borderBottom: '2px solid #e5e7eb',
//     fontSize: '14px',
//   },
//   tableRow: {
//     borderBottom: '1px solid #e5e7eb',
//   },
//   tableCell: {
//     padding: '14px',
//     color: '#1f2937',
//     fontSize: '14px',
//   },
//   statusBadge: {
//     padding: '5px 10px',
//     borderRadius: '14px',
//     fontSize: '12px',
//     fontWeight: '500',
//   },
//   statusWon: {
//     backgroundColor: '#dcfce7',
//     color: '#166534',
//   },
//   statusLost: {
//     backgroundColor: '#fee2e2',
//     color: '#991b1b',
//   },
//   statusActive: {
//     backgroundColor: '#dbeafe',
//     color: '#1e40af',
//   },
//   statusBudgetary: {
//     backgroundColor: '#fef3c7',
//     color: '#92400e',
//   },
// };

// export default CustomerAnalytics;



























// import React from 'react';
// import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
// import { Button } from '@/components/ui/button';
// import KPICard from './components/KPICard';
// import { useCustomerAnalytics, exportAnalyticsData } from './hooks/useAnalyticsData.js';
// import {
//   BarChart, Bar, PieChart, Pie, Cell,
//   XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer
// } from 'recharts';
// import { Download, Users, DollarSign, TrendingUp, UserCheck, UserPlus } from 'lucide-react';
// import { Loader2 } from 'lucide-react';

// const COLORS = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6'];

// const CustomerAnalytics = ({ filters }) => {
//   const { data, loading, error } = useCustomerAnalytics(filters);

//   const handleExport = async (format) => {
//     const result = await exportAnalyticsData('customer', format, filters);
//     if (result.success) {
//       alert(`Data exported successfully as ${format.toUpperCase()}`);
//     } else {
//       alert(`Export failed: ${result.error}`);
//     }
//   };

//   if (loading) {
//     return (
//       <div style={styles.loadingContainer}>
//         <Loader2 className="w-8 h-8 animate-spin text-blue-600" />
//         <span style={styles.loadingText}>Loading customer analytics...</span>
//       </div>
//     );
//   }

//   if (error) {
//     return (
//       <div style={styles.errorContainer}>
//         <div style={styles.errorContent}>
//           <p style={styles.errorText}>{error}</p>
//           <Button onClick={() => window.location.reload()} style={styles.retryButton}>
//             Retry
//           </Button>
//         </div>
//       </div>
//     );
//   }

//   if (!data) return null;

//   const { 
//     kpis, 
//     top_customers_by_count, 
//     top_customers_by_revenue, 
//     customer_status_breakdown, 
//     activity_timeline,
//     new_vs_repeat 
//   } = data;

//   // Prepare new vs repeat data for pie chart
//   const newVsRepeatData = [
//     { name: 'New Customers', value: new_vs_repeat.new },
//     { name: 'Repeat Customers', value: new_vs_repeat.repeat }
//   ];

//   return (
//     <div style={styles.container}>
//       {/* Export Buttons */}
//       <div style={styles.exportSection}>
//         <Button
//           variant="outline"
//           onClick={() => handleExport('json')}
//           style={styles.exportButton}
//         >
//           <Download className="w-4 h-4" />
//           <span style={styles.exportText}>Export JSON</span>
//         </Button>
//         <Button
//           variant="outline"
//           onClick={() => handleExport('csv')}
//           style={styles.exportButton}
//         >
//           <Download className="w-4 h-4" />
//           <span style={styles.exportText}>Export CSV</span>
//         </Button>
//       </div>

//       {/* KPI Cards */}
//       <div style={styles.kpiGrid}>
//         <KPICard
//           label={kpis.total_customers.label}
//           value={kpis.total_customers.value}
//           changePercent={kpis.total_customers.change_percent}
//           changeDirection={kpis.total_customers.change_direction}
//           formatType={kpis.total_customers.format_type}
//           icon={Users}
//         />
//         <KPICard
//           label={kpis.total_revenue.label}
//           value={kpis.total_revenue.value}
//           changePercent={kpis.total_revenue.change_percent}
//           changeDirection={kpis.total_revenue.change_direction}
//           formatType={kpis.total_revenue.format_type}
//           icon={DollarSign}
//         />
//         <KPICard
//           label={kpis.avg_revenue_per_customer.label}
//           value={kpis.avg_revenue_per_customer.value}
//           changePercent={kpis.avg_revenue_per_customer.change_percent}
//           changeDirection={kpis.avg_revenue_per_customer.change_direction}
//           formatType={kpis.avg_revenue_per_customer.format_type}
//           icon={TrendingUp}
//         />
//         <KPICard
//           label={kpis.new_customers.label}
//           value={kpis.new_customers.value}
//           formatType={kpis.new_customers.format_type}
//           icon={UserPlus}
//         />
//         <KPICard
//           label={kpis.repeat_customers.label}
//           value={kpis.repeat_customers.value}
//           formatType={kpis.repeat_customers.format_type}
//           icon={UserCheck}
//         />
//       </div>

//       {/* Charts Row 1 */}
//       <div style={styles.chartsRow}>
//         {/* Top Customers by Quote Count */}
//         <Card style={styles.chartCard}>
//           <CardHeader style={styles.cardHeader}>
//             <CardTitle style={styles.cardTitle}>Top Customers by Quote Count</CardTitle>
//           </CardHeader>
//           <CardContent style={styles.cardContent}>
//             <ResponsiveContainer width="100%" height={280}>
//               <BarChart data={top_customers_by_count.slice(0, 10)}>
//                 <CartesianGrid strokeDasharray="3 3" />
//                 <XAxis 
//                   dataKey="customer_name" 
//                   angle={-45}
//                   textAnchor="end"
//                   height={100}
//                   interval={0}
//                   tick={{ fontSize: 10 }}
//                 />
//                 <YAxis tick={{ fontSize: 11 }} />
//                 <Tooltip />
//                 <Legend wrapperStyle={{ fontSize: '12px' }} />
//                 <Bar dataKey="quote_count" fill="#3b82f6" name="Quotes" />
//               </BarChart>
//             </ResponsiveContainer>
//           </CardContent>
//         </Card>

//         {/* Top Customers by Revenue */}
//         <Card style={styles.chartCard}>
//           <CardHeader style={styles.cardHeader}>
//             <CardTitle style={styles.cardTitle}>Top Customers by Revenue</CardTitle>
//           </CardHeader>
//           <CardContent style={styles.cardContent}>
//             <ResponsiveContainer width="100%" height={280}>
//               <BarChart data={top_customers_by_revenue.slice(0, 10)}>
//                 <CartesianGrid strokeDasharray="3 3" />
//                 <XAxis 
//                   dataKey="customer_name" 
//                   angle={-45}
//                   textAnchor="end"
//                   height={100}
//                   interval={0}
//                   tick={{ fontSize: 10 }}
//                 />
//                 <YAxis tick={{ fontSize: 11 }} />
//                 <Tooltip formatter={(value) => `$${value.toLocaleString()}`} />
//                 <Legend wrapperStyle={{ fontSize: '12px' }} />
//                 <Bar dataKey="revenue" fill="#10b981" name="Revenue" />
//               </BarChart>
//             </ResponsiveContainer>
//           </CardContent>
//         </Card>
//       </div>

//       {/* Charts Row 2 */}
//       <div style={styles.chartsRow}>
//         {/* Customer Status Breakdown */}
//         <Card style={styles.chartCard}>
//           <CardHeader style={styles.cardHeader}>
//             <CardTitle style={styles.cardTitle}>Customer Quote Status Breakdown</CardTitle>
//           </CardHeader>
//           <CardContent style={styles.cardContent}>
//             <ResponsiveContainer width="100%" height={280}>
//               <BarChart data={customer_status_breakdown.slice(0, 10)}>
//                 <CartesianGrid strokeDasharray="3 3" />
//                 <XAxis 
//                   dataKey="customer_name"
//                   angle={-45}
//                   textAnchor="end"
//                   height={100}
//                   interval={0}
//                   tick={{ fontSize: 10 }}
//                 />
//                 <YAxis tick={{ fontSize: 11 }} />
//                 <Tooltip />
//                 <Legend wrapperStyle={{ fontSize: '11px' }} />
//                 <Bar dataKey="Budgetary" stackId="a" fill="#fbbf24" name="Budgetary" />
//                 <Bar dataKey="Active" stackId="a" fill="#3b82f6" name="Active" />
//                 <Bar dataKey="Won" stackId="a" fill="#10b981" name="Won" />
//                 <Bar dataKey="Lost" stackId="a" fill="#ef4444" name="Lost" />
//               </BarChart>
//             </ResponsiveContainer>
//           </CardContent>
//         </Card>

//         {/* New vs Repeat Customers */}
//         <Card style={styles.chartCard}>
//           <CardHeader style={styles.cardHeader}>
//             <CardTitle style={styles.cardTitle}>New vs Repeat Customers</CardTitle>
//           </CardHeader>
//           <CardContent style={styles.cardContent}>
//             <ResponsiveContainer width="100%" height={280}>
//               <PieChart>
//                 <Pie
//                   data={newVsRepeatData}
//                   dataKey="value"
//                   nameKey="name"
//                   cx="50%"
//                   cy="45%"
//                   outerRadius={80}
//                   label={(entry) => `${entry.value}`}
//                   labelLine={false}
//                 >
//                   {newVsRepeatData.map((entry, index) => (
//                     <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
//                   ))}
//                 </Pie>
//                 <Tooltip />
//                 <Legend wrapperStyle={{ fontSize: '11px' }} />
//               </PieChart>
//             </ResponsiveContainer>
//             <div style={styles.pieChartInfo}>
//               <p style={styles.pieChartText}>
//                 Total: {new_vs_repeat.total} customers
//               </p>
//               <p style={styles.pieChartText}>
//                 Repeat Rate: {((new_vs_repeat.repeat / new_vs_repeat.total) * 100).toFixed(1)}%
//               </p>
//             </div>
//           </CardContent>
//         </Card>
//       </div>

//       {/* Data Tables */}
//       <div style={styles.tableSection}>
//         {/* Top Customers Detail Table */}
//         <Card style={styles.tableCard}>
//           <CardHeader style={styles.cardHeader}>
//             <CardTitle style={styles.cardTitle}>Top Customer Performance</CardTitle>
//           </CardHeader>
//           <CardContent style={styles.cardContent}>
//             <div style={styles.tableWrapper}>
//               <table style={styles.table}>
//                 <thead>
//                   <tr style={styles.tableHeaderRow}>
//                     <th style={styles.tableHeader}>Customer Name</th>
//                     <th style={{ ...styles.tableHeader, textAlign: 'right' }}>Quotes</th>
//                     <th style={{ ...styles.tableHeader, textAlign: 'right' }}>Total Revenue</th>
//                     <th style={{ ...styles.tableHeader, textAlign: 'right' }}>Avg Deal Size</th>
//                     <th style={{ ...styles.tableHeader, textAlign: 'right' }}>Last Quote</th>
//                   </tr>
//                 </thead>
//                 <tbody>
//                   {top_customers_by_revenue.slice(0, 10).map((customer, index) => (
//                     <tr key={index} style={styles.tableRow}>
//                       <td style={styles.tableCell}>{customer.customer_name}</td>
//                       <td style={{ ...styles.tableCell, textAlign: 'right' }}>{customer.quote_count}</td>
//                       <td style={{ ...styles.tableCell, textAlign: 'right' }}>${customer.revenue.toLocaleString()}</td>
//                       <td style={{ ...styles.tableCell, textAlign: 'right' }}>${customer.avg_deal_size.toLocaleString()}</td>
//                       <td style={{ ...styles.tableCell, textAlign: 'right' }}>{customer.last_quote_date || 'N/A'}</td>
//                     </tr>
//                   ))}
//                 </tbody>
//               </table>
//             </div>
//           </CardContent>
//         </Card>

//         {/* Recent Customer Activity */}
//         <Card style={styles.tableCard}>
//           <CardHeader style={styles.cardHeader}>
//             <CardTitle style={styles.cardTitle}>Recent Customer Activity</CardTitle>
//           </CardHeader>
//           <CardContent style={styles.cardContent}>
//             <div style={styles.tableWrapper}>
//               <table style={styles.table}>
//                 <thead>
//                   <tr style={styles.tableHeaderRow}>
//                     <th style={styles.tableHeader}>Date</th>
//                     <th style={styles.tableHeader}>Customer</th>
//                     <th style={styles.tableHeader}>Quotation #</th>
//                     <th style={styles.tableHeader}>Status</th>
//                   </tr>
//                 </thead>
//                 <tbody>
//                   {activity_timeline.slice(0, 20).map((activity, index) => (
//                     <tr key={index} style={styles.tableRow}>
//                       <td style={styles.tableCell}>{activity.date}</td>
//                       <td style={styles.tableCell}>{activity.customer_name}</td>
//                       <td style={styles.tableCell}>{activity.quotation_number}</td>
//                       <td style={styles.tableCell}>
//                         <span style={{
//                           ...styles.statusBadge,
//                           ...(activity.status === 'Won' ? styles.statusWon :
//                               activity.status === 'Lost' ? styles.statusLost :
//                               activity.status === 'Active' ? styles.statusActive :
//                               styles.statusBudgetary)
//                         }}>
//                           {activity.status}
//                         </span>
//                       </td>
//                     </tr>
//                   ))}
//                 </tbody>
//               </table>
//             </div>
//           </CardContent>
//         </Card>
//       </div>
//     </div>
//   );
// };

// const styles = {
//   container: {
//     width: '100%',
//     maxHeight: 'calc(100vh - 300px)',
//     overflowY: 'auto',
//     overflowX: 'hidden',
//     padding: '0 4px',
//   },
//   loadingContainer: {
//     display: 'flex',
//     alignItems: 'center',
//     justifyContent: 'center',
//     height: '400px',
//     flexDirection: 'column',
//     gap: '12px',
//   },
//   loadingText: {
//     color: '#6b7280',
//     fontSize: '14px',
//   },
//   errorContainer: {
//     display: 'flex',
//     alignItems: 'center',
//     justifyContent: 'center',
//     height: '400px',
//   },
//   errorContent: {
//     textAlign: 'center',
//   },
//   errorText: {
//     color: '#dc2626',
//     fontWeight: '500',
//     marginBottom: '16px',
//   },
//   retryButton: {
//     marginTop: '16px',
//   },
//   exportSection: {
//     display: 'flex',
//     justifyContent: 'flex-end',
//     gap: '8px',
//     marginBottom: '20px',
//   },
//   exportButton: {
//     display: 'flex',
//     alignItems: 'center',
//     gap: '8px',
//     padding: '8px 16px',
//     fontSize: '13px',
//   },
//   exportText: {
//     marginLeft: '4px',
//   },
//   kpiGrid: {
//     display: 'grid',
//     gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))',
//     gap: '16px',
//     marginBottom: '24px',
//   },
//   chartsRow: {
//     display: 'grid',
//     gridTemplateColumns: 'repeat(auto-fit, minmax(500px, 1fr))',
//     gap: '20px',
//     marginBottom: '24px',
//   },
//   chartCard: {
//     boxShadow: '0 1px 3px rgba(0,0,0,0.1)',
//     borderRadius: '8px',
//   },
//   cardHeader: {
//     padding: '16px',
//     borderBottom: '1px solid #e5e7eb',
//   },
//   cardTitle: {
//     fontSize: '16px',
//     fontWeight: '600',
//     color: '#1f2937',
//   },
//   cardContent: {
//     padding: '16px',
//   },
//   pieChartInfo: {
//     marginTop: '16px',
//     textAlign: 'center',
//   },
//   pieChartText: {
//     fontSize: '13px',
//     color: '#6b7280',
//     margin: '4px 0',
//   },
//   tableSection: {
//     display: 'grid',
//     gridTemplateColumns: '1fr',
//     gap: '20px',
//     marginBottom: '24px',
//   },
//   tableCard: {
//     boxShadow: '0 1px 3px rgba(0,0,0,0.1)',
//     borderRadius: '8px',
//   },
//   tableWrapper: {
//     overflowX: 'auto',
//     maxHeight: '350px',
//     overflowY: 'auto',
//   },
//   table: {
//     width: '100%',
//     borderCollapse: 'collapse',
//     fontSize: '13px',
//   },
//   tableHeaderRow: {
//     backgroundColor: '#f9fafb',
//     position: 'sticky',
//     top: 0,
//     zIndex: 1,
//   },
//   tableHeader: {
//     padding: '12px',
//     textAlign: 'left',
//     fontWeight: '600',
//     color: '#374151',
//     borderBottom: '2px solid #e5e7eb',
//   },
//   tableRow: {
//     borderBottom: '1px solid #e5e7eb',
//   },
//   tableCell: {
//     padding: '12px',
//     color: '#1f2937',
//   },
//   statusBadge: {
//     padding: '4px 8px',
//     borderRadius: '12px',
//     fontSize: '11px',
//     fontWeight: '500',
//   },
//   statusWon: {
//     backgroundColor: '#dcfce7',
//     color: '#166534',
//   },
//   statusLost: {
//     backgroundColor: '#fee2e2',
//     color: '#991b1b',
//   },
//   statusActive: {
//     backgroundColor: '#dbeafe',
//     color: '#1e40af',
//   },
//   statusBudgetary: {
//     backgroundColor: '#fef3c7',
//     color: '#92400e',
//   },
// };

// export default CustomerAnalytics;


