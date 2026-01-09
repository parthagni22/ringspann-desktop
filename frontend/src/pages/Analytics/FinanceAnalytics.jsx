import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import KPICard from './components/KPICard';
import FinanceFilterPanel from './components/FinanceFilterPanel';
import { useFinanceAnalytics, exportAnalyticsData } from './hooks/useAnalyticsData.js';
import {
  BarChart, Bar, LineChart, Line,
  XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer
} from 'recharts';
import { Download, DollarSign, FileText, TrendingUp, Package } from 'lucide-react';
import { Loader2 } from 'lucide-react';

const FinanceAnalytics = ({ filters, onFilterChange }) => {
  const { data, loading, error } = useFinanceAnalytics(filters);

  const handleExport = async (format) => {
    const result = await exportAnalyticsData('finance', format, filters);
    if (result.success) {
      alert(`Data exported successfully as ${format.toUpperCase()}`);
    } else {
      alert(`Export failed: ${result.error}`);
    }
  };

  if (loading) {
    return (
      <div style={styles.loadingContainer}>
        <Loader2 className="w-8 h-8 animate-spin text-blue-600" />
        <span style={styles.loadingText}>Loading finance analytics...</span>
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

  const { kpis, revenue_by_status, monthly_trend, product_revenue, value_distribution } = data;

  return (
    <div style={styles.container}>
      {/* Tab-Specific Finance Filter Panel */}
      <FinanceFilterPanel filters={filters} onFilterChange={onFilterChange} />

      {/* Export Buttons */}
      <div style={styles.exportSection}>
        <Button
          variant="outline"
          onClick={() => handleExport('json')}
          style={styles.exportButton}
        >
          <Download className="w-4 h-4" />
          <span style={styles.exportText}>Export JSON</span>
        </Button>
        <Button
          variant="outline"
          onClick={() => handleExport('csv')}
          style={styles.exportButton}
        >
          <Download className="w-4 h-4" />
          <span style={styles.exportText}>Export CSV</span>
        </Button>
      </div>

      {/* KPI Cards */}
      <div style={styles.kpiGrid}>
        <KPICard
          label={kpis.total_quoted_value.label}
          value={kpis.total_quoted_value.value}
          changePercent={kpis.total_quoted_value.change_percent}
          changeDirection={kpis.total_quoted_value.change_direction}
          formatType={kpis.total_quoted_value.format_type}
          icon={DollarSign}
        />
        <KPICard
          label={kpis.total_quotes.label}
          value={kpis.total_quotes.value}
          changePercent={kpis.total_quotes.change_percent}
          changeDirection={kpis.total_quotes.change_direction}
          formatType={kpis.total_quotes.format_type}
          icon={FileText}
        />
        <KPICard
          label={kpis.avg_quote_value.label}
          value={kpis.avg_quote_value.value}
          changePercent={kpis.avg_quote_value.change_percent}
          changeDirection={kpis.avg_quote_value.change_direction}
          formatType={kpis.avg_quote_value.format_type}
          icon={TrendingUp}
        />
        <KPICard
          label={kpis.top_product.label}
          value={kpis.top_product.value}
          formatType="text"
          icon={Package}
        />
        <KPICard
          label={kpis.top_product_revenue.label}
          value={kpis.top_product_revenue.value}
          formatType={kpis.top_product_revenue.format_type}
          icon={DollarSign}
        />
      </div>

      {/* Charts Row 1 */}
      <div style={styles.chartsRow}>
        {/* Revenue by Status */}
        <Card style={styles.chartCard}>
          <CardHeader style={styles.cardHeader}>
            <CardTitle style={styles.cardTitle}>Revenue by Quote Status</CardTitle>
          </CardHeader>
          <CardContent style={styles.cardContent}>
            <ResponsiveContainer width="100%" height={400}>
              <BarChart data={revenue_by_status}>
                <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
                <XAxis dataKey="label" tick={{ fontSize: 13, fill: '#374151' }} />
                <YAxis tick={{ fontSize: 13, fill: '#374151' }} />
                <Tooltip formatter={(value) => `$${value.toLocaleString()}`} contentStyle={{ fontSize: '14px' }} />
                <Legend wrapperStyle={{ fontSize: '14px', paddingTop: '10px' }} />
                <Bar dataKey="value" fill="#10b981" name="Revenue" radius={[6, 6, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        {/* Product Revenue Breakdown - VERTICAL with scroll */}
        <Card style={styles.chartCard}>
          <CardHeader style={styles.cardHeader}>
            <CardTitle style={styles.cardTitle}>Revenue by Product Type</CardTitle>
          </CardHeader>
          <CardContent style={styles.cardContent}>
            <div style={styles.chartScrollWrapperVertical}>
              <div style={{ minHeight: Math.max(400, product_revenue.length * 40) }}>
                <ResponsiveContainer width="100%" height={Math.max(400, product_revenue.length * 40)}>
                  <BarChart data={product_revenue} layout="vertical">
                    <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
                    <XAxis type="number" tick={{ fontSize: 13, fill: '#374151' }} />
                    <YAxis 
                      dataKey="product_type" 
                      type="category" 
                      width={200}
                      tick={{ fontSize: 13, fill: '#374151' }}
                      interval={0}
                    />
                    <Tooltip formatter={(value) => `$${value.toLocaleString()}`} contentStyle={{ fontSize: '14px' }} />
                    <Legend wrapperStyle={{ fontSize: '14px' }} />
                    <Bar dataKey="revenue" fill="#10b981" name="Revenue" radius={[0, 6, 6, 0]} />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Charts Row 2 */}
      <div style={styles.chartsRow}>
        {/* Monthly Revenue Trend */}
        <Card style={styles.chartCard}>
          <CardHeader style={styles.cardHeader}>
            <CardTitle style={styles.cardTitle}>Monthly Revenue Trend</CardTitle>
          </CardHeader>
          <CardContent style={styles.cardContent}>
            <ResponsiveContainer width="100%" height={400}>
              <LineChart data={monthly_trend}>
                <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
                <XAxis dataKey="date" tick={{ fontSize: 13, fill: '#374151' }} />
                <YAxis tick={{ fontSize: 13, fill: '#374151' }} />
                <Tooltip formatter={(value) => `$${value.toLocaleString()}`} contentStyle={{ fontSize: '14px' }} />
                <Legend wrapperStyle={{ fontSize: '14px', paddingTop: '10px' }} />
                <Line 
                  type="monotone" 
                  dataKey="value" 
                  stroke="#10b981" 
                  strokeWidth={3}
                  name="Revenue"
                  dot={{ r: 5, fill: '#10b981' }}
                  activeDot={{ r: 7 }}
                />
              </LineChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        {/* Quote Value Distribution */}
        <Card style={styles.chartCard}>
          <CardHeader style={styles.cardHeader}>
            <CardTitle style={styles.cardTitle}>Quote Value Distribution</CardTitle>
          </CardHeader>
          <CardContent style={styles.cardContent}>
            <ResponsiveContainer width="100%" height={400}>
              <BarChart data={value_distribution}>
                <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
                <XAxis 
                  dataKey="range" 
                  angle={-45}
                  textAnchor="end"
                  height={120}
                  interval={0}
                  tick={{ fontSize: 12, fill: '#374151' }}
                />
                <YAxis tick={{ fontSize: 13, fill: '#374151' }} />
                <Tooltip contentStyle={{ fontSize: '14px' }} />
                <Legend wrapperStyle={{ fontSize: '14px', paddingTop: '10px' }} />
                <Bar dataKey="count" fill="#8b5cf6" name="Quote Count" radius={[6, 6, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>
      </div>

      {/* Data Tables */}
      <div style={styles.tablesRow}>
        {/* Revenue by Status Table */}
        <Card style={styles.tableCard}>
          <CardHeader style={styles.cardHeader}>
            <CardTitle style={styles.cardTitle}>Status Breakdown</CardTitle>
          </CardHeader>
          <CardContent style={styles.cardContent}>
            <div style={styles.tableWrapper}>
              <table style={styles.table}>
                <thead>
                  <tr style={styles.tableHeaderRow}>
                    <th style={styles.tableHeader}>Status</th>
                    <th style={{ ...styles.tableHeader, textAlign: 'right' }}>Quotes</th>
                    <th style={{ ...styles.tableHeader, textAlign: 'right' }}>Revenue</th>
                    <th style={{ ...styles.tableHeader, textAlign: 'right' }}>Avg Value</th>
                  </tr>
                </thead>
                <tbody>
                  {revenue_by_status.map((item, index) => (
                    <tr key={index} style={styles.tableRow}>
                      <td style={styles.tableCell}>{item.label}</td>
                      <td style={{ ...styles.tableCell, textAlign: 'right' }}>{item.metadata.quote_count}</td>
                      <td style={{ ...styles.tableCell, textAlign: 'right' }}>${item.value.toLocaleString()}</td>
                      <td style={{ ...styles.tableCell, textAlign: 'right' }}>
                        ${item.metadata.avg_revenue.toLocaleString()}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </CardContent>
        </Card>

        {/* Product Revenue Table */}
        <Card style={styles.tableCard}>
          <CardHeader style={styles.cardHeader}>
            <CardTitle style={styles.cardTitle}>Product Performance</CardTitle>
          </CardHeader>
          <CardContent style={styles.cardContent}>
            <div style={styles.tableWrapper}>
              <table style={styles.table}>
                <thead>
                  <tr style={styles.tableHeaderRow}>
                    <th style={styles.tableHeader}>Product</th>
                    <th style={{ ...styles.tableHeader, textAlign: 'right' }}>Quotes</th>
                    <th style={{ ...styles.tableHeader, textAlign: 'right' }}>Revenue</th>
                    <th style={{ ...styles.tableHeader, textAlign: 'right' }}>%</th>
                  </tr>
                </thead>
                <tbody>
                  {product_revenue.map((product, index) => (
                    <tr key={index} style={styles.tableRow}>
                      <td style={styles.tableCell}>{product.product_type}</td>
                      <td style={{ ...styles.tableCell, textAlign: 'right' }}>{product.quote_count}</td>
                      <td style={{ ...styles.tableCell, textAlign: 'right' }}>${product.revenue.toLocaleString()}</td>
                      <td style={{ ...styles.tableCell, textAlign: 'right' }}>{product.percentage.toFixed(1)}%</td>
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
  tablesRow: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(500px, 1fr))',
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
  chartScrollWrapperVertical: {
    overflowY: 'auto',
    overflowX: 'hidden',
    maxHeight: '500px',
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
};

export default FinanceAnalytics;


































// import React from 'react';
// import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
// import { Button } from '@/components/ui/button';
// import KPICard from './components/KPICard';
// import { useFinanceAnalytics, exportAnalyticsData } from './hooks/useAnalyticsData.js';
// import {
//   BarChart, Bar, LineChart, Line,
//   XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer
// } from 'recharts';
// import { Download, DollarSign, FileText, TrendingUp, Package } from 'lucide-react';
// import { Loader2 } from 'lucide-react';

// const FinanceAnalytics = ({ filters }) => {
//   const { data, loading, error } = useFinanceAnalytics(filters);

//   const handleExport = async (format) => {
//     const result = await exportAnalyticsData('finance', format, filters);
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
//         <span style={styles.loadingText}>Loading finance analytics...</span>
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

//   const { kpis, revenue_by_status, monthly_trend, product_revenue, value_distribution } = data;

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
//           label={kpis.total_quoted_value.label}
//           value={kpis.total_quoted_value.value}
//           changePercent={kpis.total_quoted_value.change_percent}
//           changeDirection={kpis.total_quoted_value.change_direction}
//           formatType={kpis.total_quoted_value.format_type}
//           icon={DollarSign}
//         />
//         <KPICard
//           label={kpis.total_quotes.label}
//           value={kpis.total_quotes.value}
//           changePercent={kpis.total_quotes.change_percent}
//           changeDirection={kpis.total_quotes.change_direction}
//           formatType={kpis.total_quotes.format_type}
//           icon={FileText}
//         />
//         <KPICard
//           label={kpis.avg_quote_value.label}
//           value={kpis.avg_quote_value.value}
//           changePercent={kpis.avg_quote_value.change_percent}
//           changeDirection={kpis.avg_quote_value.change_direction}
//           formatType={kpis.avg_quote_value.format_type}
//           icon={TrendingUp}
//         />
//         <KPICard
//           label={kpis.top_product.label}
//           value={kpis.top_product.value}
//           formatType="text"
//           icon={Package}
//         />
//         <KPICard
//           label={kpis.top_product_revenue.label}
//           value={kpis.top_product_revenue.value}
//           formatType={kpis.top_product_revenue.format_type}
//           icon={DollarSign}
//         />
//       </div>

//       {/* Charts Row 1 */}
//       <div style={styles.chartsRow}>
//         {/* Revenue by Status */}
//         <Card style={styles.chartCard}>
//           <CardHeader style={styles.cardHeader}>
//             <CardTitle style={styles.cardTitle}>Revenue by Quote Status</CardTitle>
//           </CardHeader>
//           <CardContent style={styles.cardContent}>
//             <ResponsiveContainer width="100%" height={400}>
//               <BarChart data={revenue_by_status}>
//                 <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
//                 <XAxis dataKey="label" tick={{ fontSize: 13, fill: '#374151' }} />
//                 <YAxis tick={{ fontSize: 13, fill: '#374151' }} />
//                 <Tooltip formatter={(value) => `$${value.toLocaleString()}`} contentStyle={{ fontSize: '14px' }} />
//                 <Legend wrapperStyle={{ fontSize: '14px', paddingTop: '10px' }} />
//                 <Bar dataKey="value" fill="#3b82f6" name="Revenue" radius={[6, 6, 0, 0]} />
//               </BarChart>
//             </ResponsiveContainer>
//           </CardContent>
//         </Card>

//         {/* Product Revenue Breakdown - VERTICAL with scroll */}
//         <Card style={styles.chartCard}>
//           <CardHeader style={styles.cardHeader}>
//             <CardTitle style={styles.cardTitle}>Revenue by Product Type</CardTitle>
//           </CardHeader>
//           <CardContent style={styles.cardContent}>
//             <div style={styles.chartScrollWrapperVertical}>
//               <div style={{ minHeight: Math.max(400, product_revenue.length * 40) }}>
//                 <ResponsiveContainer width="100%" height={Math.max(400, product_revenue.length * 40)}>
//                   <BarChart data={product_revenue} layout="vertical">
//                     <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
//                     <XAxis type="number" tick={{ fontSize: 13, fill: '#374151' }} />
//                     <YAxis 
//                       dataKey="product_type" 
//                       type="category" 
//                       width={200}
//                       tick={{ fontSize: 13, fill: '#374151' }}
//                       interval={0}
//                     />
//                     <Tooltip formatter={(value) => `$${value.toLocaleString()}`} contentStyle={{ fontSize: '14px' }} />
//                     <Legend wrapperStyle={{ fontSize: '14px' }} />
//                     <Bar dataKey="revenue" fill="#10b981" name="Revenue" radius={[0, 6, 6, 0]} />
//                   </BarChart>
//                 </ResponsiveContainer>
//               </div>
//             </div>
//           </CardContent>
//         </Card>
//       </div>

//       {/* Charts Row 2 */}
//       <div style={styles.chartsRow}>
//         {/* Monthly Revenue Trend */}
//         <Card style={styles.chartCard}>
//           <CardHeader style={styles.cardHeader}>
//             <CardTitle style={styles.cardTitle}>Monthly Revenue Trend</CardTitle>
//           </CardHeader>
//           <CardContent style={styles.cardContent}>
//             <ResponsiveContainer width="100%" height={400}>
//               <LineChart data={monthly_trend}>
//                 <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
//                 <XAxis dataKey="date" tick={{ fontSize: 13, fill: '#374151' }} />
//                 <YAxis tick={{ fontSize: 13, fill: '#374151' }} />
//                 <Tooltip formatter={(value) => `$${value.toLocaleString()}`} contentStyle={{ fontSize: '14px' }} />
//                 <Legend wrapperStyle={{ fontSize: '14px', paddingTop: '10px' }} />
//                 <Line 
//                   type="monotone" 
//                   dataKey="value" 
//                   stroke="#3b82f6" 
//                   strokeWidth={3}
//                   name="Revenue"
//                   dot={{ r: 5, fill: '#3b82f6' }}
//                   activeDot={{ r: 7 }}
//                 />
//               </LineChart>
//             </ResponsiveContainer>
//           </CardContent>
//         </Card>

//         {/* Quote Value Distribution */}
//         <Card style={styles.chartCard}>
//           <CardHeader style={styles.cardHeader}>
//             <CardTitle style={styles.cardTitle}>Quote Value Distribution</CardTitle>
//           </CardHeader>
//           <CardContent style={styles.cardContent}>
//             <ResponsiveContainer width="100%" height={400}>
//               <BarChart data={value_distribution}>
//                 <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
//                 <XAxis 
//                   dataKey="range" 
//                   angle={-45}
//                   textAnchor="end"
//                   height={120}
//                   interval={0}
//                   tick={{ fontSize: 12, fill: '#374151' }}
//                 />
//                 <YAxis tick={{ fontSize: 13, fill: '#374151' }} />
//                 <Tooltip contentStyle={{ fontSize: '14px' }} />
//                 <Legend wrapperStyle={{ fontSize: '14px', paddingTop: '10px' }} />
//                 <Bar dataKey="count" fill="#8b5cf6" name="Quote Count" radius={[6, 6, 0, 0]} />
//               </BarChart>
//             </ResponsiveContainer>
//           </CardContent>
//         </Card>
//       </div>

//       {/* Data Tables */}
//       <div style={styles.tablesRow}>
//         {/* Revenue by Status Table */}
//         <Card style={styles.tableCard}>
//           <CardHeader style={styles.cardHeader}>
//             <CardTitle style={styles.cardTitle}>Status Breakdown</CardTitle>
//           </CardHeader>
//           <CardContent style={styles.cardContent}>
//             <div style={styles.tableWrapper}>
//               <table style={styles.table}>
//                 <thead>
//                   <tr style={styles.tableHeaderRow}>
//                     <th style={styles.tableHeader}>Status</th>
//                     <th style={{ ...styles.tableHeader, textAlign: 'right' }}>Quotes</th>
//                     <th style={{ ...styles.tableHeader, textAlign: 'right' }}>Revenue</th>
//                     <th style={{ ...styles.tableHeader, textAlign: 'right' }}>Avg Value</th>
//                   </tr>
//                 </thead>
//                 <tbody>
//                   {revenue_by_status.map((item, index) => (
//                     <tr key={index} style={styles.tableRow}>
//                       <td style={styles.tableCell}>{item.label}</td>
//                       <td style={{ ...styles.tableCell, textAlign: 'right' }}>{item.metadata.quote_count}</td>
//                       <td style={{ ...styles.tableCell, textAlign: 'right' }}>${item.value.toLocaleString()}</td>
//                       <td style={{ ...styles.tableCell, textAlign: 'right' }}>
//                         ${item.metadata.avg_revenue.toLocaleString()}
//                       </td>
//                     </tr>
//                   ))}
//                 </tbody>
//               </table>
//             </div>
//           </CardContent>
//         </Card>

//         {/* Product Revenue Table */}
//         <Card style={styles.tableCard}>
//           <CardHeader style={styles.cardHeader}>
//             <CardTitle style={styles.cardTitle}>Product Performance</CardTitle>
//           </CardHeader>
//           <CardContent style={styles.cardContent}>
//             <div style={styles.tableWrapper}>
//               <table style={styles.table}>
//                 <thead>
//                   <tr style={styles.tableHeaderRow}>
//                     <th style={styles.tableHeader}>Product</th>
//                     <th style={{ ...styles.tableHeader, textAlign: 'right' }}>Quotes</th>
//                     <th style={{ ...styles.tableHeader, textAlign: 'right' }}>Revenue</th>
//                     <th style={{ ...styles.tableHeader, textAlign: 'right' }}>%</th>
//                   </tr>
//                 </thead>
//                 <tbody>
//                   {product_revenue.map((product, index) => (
//                     <tr key={index} style={styles.tableRow}>
//                       <td style={styles.tableCell}>{product.product_type}</td>
//                       <td style={{ ...styles.tableCell, textAlign: 'right' }}>{product.quote_count}</td>
//                       <td style={{ ...styles.tableCell, textAlign: 'right' }}>${product.revenue.toLocaleString()}</td>
//                       <td style={{ ...styles.tableCell, textAlign: 'right' }}>{product.percentage.toFixed(1)}%</td>
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
//   tablesRow: {
//     display: 'grid',
//     gridTemplateColumns: 'repeat(auto-fit, minmax(500px, 1fr))',
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
//   chartScrollWrapperVertical: {
//     overflowY: 'auto',
//     overflowX: 'hidden',
//     maxHeight: '500px',
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
// };

// export default FinanceAnalytics;






























//------------------------------------------------------------------------------------------------

// import React from 'react';
// import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
// import { Button } from '@/components/ui/button';
// import KPICard from './components/KPICard';
// import { useFinanceAnalytics, exportAnalyticsData } from './hooks/useAnalyticsData.js';
// import {
//   BarChart, Bar, LineChart, Line,
//   XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer
// } from 'recharts';
// import { Download, DollarSign, FileText, TrendingUp, Package } from 'lucide-react';
// import { Loader2 } from 'lucide-react';

// const FinanceAnalytics = ({ filters }) => {
//   const { data, loading, error } = useFinanceAnalytics(filters);

//   const handleExport = async (format) => {
//     const result = await exportAnalyticsData('finance', format, filters);
//     if (result.success) {
//       alert(`Data exported successfully as ${format.toUpperCase()}`);
//     } else {
//       alert(`Export failed: ${result.error}`);
//     }
//   };

//   if (loading) {
//     return (
//       <div className="flex items-center justify-center h-96">
//         <Loader2 className="w-8 h-8 animate-spin text-blue-600" />
//         <span className="ml-2 text-gray-600">Loading finance analytics...</span>
//       </div>
//     );
//   }

//   if (error) {
//     return (
//       <div className="flex items-center justify-center h-96">
//         <div className="text-center">
//           <p className="text-red-600 font-medium">{error}</p>
//           <Button onClick={() => window.location.reload()} className="mt-4">
//             Retry
//           </Button>
//         </div>
//       </div>
//     );
//   }

//   if (!data) return null;

//   const { kpis, revenue_by_status, monthly_trend, product_revenue, value_distribution } = data;

//   return (
//     <div className="space-y-6">
//       {/* Export Buttons */}
//       <div className="flex justify-end gap-2">
//         <Button
//           variant="outline"
//           onClick={() => handleExport('json')}
//           className="flex items-center gap-2"
//         >
//           <Download className="w-4 h-4" />
//           Export JSON
//         </Button>
//         <Button
//           variant="outline"
//           onClick={() => handleExport('csv')}
//           className="flex items-center gap-2"
//         >
//           <Download className="w-4 h-4" />
//           Export CSV
//         </Button>
//       </div>

//       {/* KPI Cards */}
//       <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4">
//         <KPICard
//           label={kpis.total_quoted_value.label}
//           value={kpis.total_quoted_value.value}
//           changePercent={kpis.total_quoted_value.change_percent}
//           changeDirection={kpis.total_quoted_value.change_direction}
//           formatType={kpis.total_quoted_value.format_type}
//           icon={DollarSign}
//         />
//         <KPICard
//           label={kpis.total_quotes.label}
//           value={kpis.total_quotes.value}
//           changePercent={kpis.total_quotes.change_percent}
//           changeDirection={kpis.total_quotes.change_direction}
//           formatType={kpis.total_quotes.format_type}
//           icon={FileText}
//         />
//         <KPICard
//           label={kpis.avg_quote_value.label}
//           value={kpis.avg_quote_value.value}
//           changePercent={kpis.avg_quote_value.change_percent}
//           changeDirection={kpis.avg_quote_value.change_direction}
//           formatType={kpis.avg_quote_value.format_type}
//           icon={TrendingUp}
//         />
//         <KPICard
//           label={kpis.top_product.label}
//           value={kpis.top_product.value}
//           formatType="text"
//           icon={Package}
//         />
//         <KPICard
//           label={kpis.top_product_revenue.label}
//           value={kpis.top_product_revenue.value}
//           formatType={kpis.top_product_revenue.format_type}
//           icon={DollarSign}
//         />
//       </div>

//       {/* Charts Row 1 */}
//       <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
//         {/* Revenue by Status */}
//         <Card>
//           <CardHeader>
//             <CardTitle>Revenue by Quote Status</CardTitle>
//           </CardHeader>
//           <CardContent>
//             <ResponsiveContainer width="100%" height={300}>
//               <BarChart data={revenue_by_status}>
//                 <CartesianGrid strokeDasharray="3 3" />
//                 <XAxis dataKey="label" />
//                 <YAxis />
//                 <Tooltip formatter={(value) => `$${value.toLocaleString()}`} />
//                 <Legend />
//                 <Bar dataKey="value" fill="#3b82f6" name="Revenue" />
//               </BarChart>
//             </ResponsiveContainer>
//           </CardContent>
//         </Card>

//         {/* Product Revenue Breakdown */}
//         <Card>
//           <CardHeader>
//             <CardTitle>Revenue by Product Type</CardTitle>
//           </CardHeader>
//           <CardContent>
//             <ResponsiveContainer width="100%" height={300}>
//               <BarChart data={product_revenue} layout="vertical">
//                 <CartesianGrid strokeDasharray="3 3" />
//                 <XAxis type="number" />
//                 <YAxis 
//                   dataKey="product_type" 
//                   type="category" 
//                   width={150}
//                   tick={{ fontSize: 12 }}
//                 />
//                 <Tooltip formatter={(value) => `$${value.toLocaleString()}`} />
//                 <Legend />
//                 <Bar dataKey="revenue" fill="#10b981" name="Revenue" />
//               </BarChart>
//             </ResponsiveContainer>
//           </CardContent>
//         </Card>
//       </div>

//       {/* Charts Row 2 */}
//       <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
//         {/* Monthly Revenue Trend */}
//         <Card>
//           <CardHeader>
//             <CardTitle>Monthly Revenue Trend</CardTitle>
//           </CardHeader>
//           <CardContent>
//             <ResponsiveContainer width="100%" height={300}>
//               <LineChart data={monthly_trend}>
//                 <CartesianGrid strokeDasharray="3 3" />
//                 <XAxis dataKey="date" />
//                 <YAxis />
//                 <Tooltip formatter={(value) => `$${value.toLocaleString()}`} />
//                 <Legend />
//                 <Line 
//                   type="monotone" 
//                   dataKey="value" 
//                   stroke="#3b82f6" 
//                   strokeWidth={2}
//                   name="Revenue"
//                   dot={{ r: 4 }}
//                 />
//               </LineChart>
//             </ResponsiveContainer>
//           </CardContent>
//         </Card>

//         {/* Quote Value Distribution */}
//         <Card>
//           <CardHeader>
//             <CardTitle>Quote Value Distribution</CardTitle>
//           </CardHeader>
//           <CardContent>
//             <ResponsiveContainer width="100%" height={300}>
//               <BarChart data={value_distribution}>
//                 <CartesianGrid strokeDasharray="3 3" />
//                 <XAxis 
//                   dataKey="range" 
//                   angle={-45}
//                   textAnchor="end"
//                   height={100}
//                   interval={0}
//                   tick={{ fontSize: 10 }}
//                 />
//                 <YAxis />
//                 <Tooltip />
//                 <Legend />
//                 <Bar dataKey="count" fill="#8b5cf6" name="Quote Count" />
//               </BarChart>
//             </ResponsiveContainer>
//           </CardContent>
//         </Card>
//       </div>

//       {/* Data Tables */}
//       <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
//         {/* Revenue by Status Table */}
//         <Card>
//           <CardHeader>
//             <CardTitle>Status Breakdown</CardTitle>
//           </CardHeader>
//           <CardContent>
//             <div className="overflow-x-auto">
//               <table className="w-full text-sm">
//                 <thead>
//                   <tr className="border-b">
//                     <th className="text-left p-2">Status</th>
//                     <th className="text-right p-2">Quotes</th>
//                     <th className="text-right p-2">Revenue</th>
//                     <th className="text-right p-2">Avg Value</th>
//                   </tr>
//                 </thead>
//                 <tbody>
//                   {revenue_by_status.map((item, index) => (
//                     <tr key={index} className="border-b hover:bg-gray-50">
//                       <td className="p-2 font-medium">{item.label}</td>
//                       <td className="text-right p-2">{item.metadata.quote_count}</td>
//                       <td className="text-right p-2">${item.value.toLocaleString()}</td>
//                       <td className="text-right p-2">
//                         ${item.metadata.avg_revenue.toLocaleString()}
//                       </td>
//                     </tr>
//                   ))}
//                 </tbody>
//               </table>
//             </div>
//           </CardContent>
//         </Card>

//         {/* Product Revenue Table */}
//         <Card>
//           <CardHeader>
//             <CardTitle>Product Performance</CardTitle>
//           </CardHeader>
//           <CardContent>
//             <div className="overflow-x-auto">
//               <table className="w-full text-sm">
//                 <thead>
//                   <tr className="border-b">
//                     <th className="text-left p-2">Product</th>
//                     <th className="text-right p-2">Quotes</th>
//                     <th className="text-right p-2">Revenue</th>
//                     <th className="text-right p-2">%</th>
//                   </tr>
//                 </thead>
//                 <tbody>
//                   {product_revenue.slice(0, 5).map((product, index) => (
//                     <tr key={index} className="border-b hover:bg-gray-50">
//                       <td className="p-2 font-medium">{product.product_type}</td>
//                       <td className="text-right p-2">{product.quote_count}</td>
//                       <td className="text-right p-2">${product.revenue.toLocaleString()}</td>
//                       <td className="text-right p-2">{product.percentage.toFixed(1)}%</td>
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

// export default FinanceAnalytics;