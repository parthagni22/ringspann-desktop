import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import CombinedInsightsFilterPanel from './components/CombinedInsightsFilterPanel';
import { useCombinedInsights, exportAnalyticsData } from './hooks/useAnalyticsData.js';
import {
  BarChart, Bar, LineChart, Line, AreaChart, Area,
  XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, Cell
} from 'recharts';
import { Download, TrendingUp, Filter } from 'lucide-react';
import { Loader2 } from 'lucide-react';

const COLORS = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#ec4899', '#14b8a6', '#f97316', '#06b6d4', '#84cc16'];

const CombinedInsights = ({ filters, onFilterChange }) => {
  const { data, loading, error } = useCombinedInsights(filters);

  const handleExport = async () => {
    const result = await exportAnalyticsData('combined', 'csv', filters);
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
        <span style={styles.loadingText}>Loading combined insights...</span>
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
    product_customer_matrix, 
    top_combinations, 
    funnel, 
    velocity, 
    avg_processing_time,
    product_mix_trend 
  } = data;

  return (
    <div style={styles.container}>
      {/* Tab-Specific Combined Insights Filter Panel */}
      <CombinedInsightsFilterPanel filters={filters} onFilterChange={onFilterChange} />

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

      {/* Key Metrics Card */}
      <Card style={styles.metricsCard}>
        <CardHeader style={styles.cardHeader}>
          <CardTitle style={styles.cardTitle}>Key Insights</CardTitle>
        </CardHeader>
        <CardContent style={styles.cardContent}>
          <div style={styles.metricsGrid}>
            <div style={{ ...styles.metricBox, ...styles.metricBlue }}>
              <p style={styles.metricLabel}>Avg Processing Time</p>
              <p style={styles.metricValue}>
                {avg_processing_time ? `${avg_processing_time.toFixed(1)} hrs` : 'N/A'}
              </p>
            </div>
            <div style={{ ...styles.metricBox, ...styles.metricGreen }}>
              <p style={styles.metricLabel}>Total Product-Customer Combos</p>
              <p style={styles.metricValue}>
                {top_combinations.length}
              </p>
            </div>
            <div style={{ ...styles.metricBox, ...styles.metricPurple }}>
              <p style={styles.metricLabel}>Active Products</p>
              <p style={styles.metricValue}>
                {product_customer_matrix.products?.length || 0}
              </p>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Charts Row 1 */}
      <div style={styles.chartsRow}>
        {/* Quote Status Funnel */}
        <Card style={styles.chartCard}>
          <CardHeader style={styles.cardHeader}>
            <CardTitle style={styles.cardTitle}>Quote Status Funnel</CardTitle>
          </CardHeader>
          <CardContent style={styles.cardContent}>
            <ResponsiveContainer width="100%" height={400}>
              <BarChart data={funnel} layout="horizontal">
                <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
                <XAxis type="number" tick={{ fontSize: 13, fill: '#374151' }} />
                <YAxis dataKey="stage" type="category" width={120} tick={{ fontSize: 13, fill: '#374151' }} />
                <Tooltip contentStyle={{ fontSize: '14px' }} />
                <Legend wrapperStyle={{ fontSize: '14px', paddingTop: '10px' }} />
                <Bar dataKey="count" fill="#8b5cf6" name="Quote Count" radius={[0, 6, 6, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        {/* Monthly Quote Velocity */}
        <Card style={styles.chartCard}>
          <CardHeader style={styles.cardHeader}>
            <CardTitle style={styles.cardTitle}>Monthly Quote Velocity</CardTitle>
          </CardHeader>
          <CardContent style={styles.cardContent}>
            <ResponsiveContainer width="100%" height={400}>
              <LineChart data={velocity}>
                <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
                <XAxis dataKey="date" tick={{ fontSize: 13, fill: '#374151' }} />
                <YAxis tick={{ fontSize: 13, fill: '#374151' }} />
                <Tooltip contentStyle={{ fontSize: '14px' }} />
                <Legend wrapperStyle={{ fontSize: '14px', paddingTop: '10px' }} />
                <Line 
                  type="monotone" 
                  dataKey="value" 
                  stroke="#10b981" 
                  strokeWidth={3}
                  name="Quotes Created"
                  dot={{ r: 5, fill: '#10b981' }}
                  activeDot={{ r: 7 }}
                />
              </LineChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>
      </div>

      {/* Product Mix Trend */}
      <Card style={styles.fullWidthCard}>
        <CardHeader style={styles.cardHeader}>
          <CardTitle style={styles.cardTitle}>Product Mix Trend Over Time</CardTitle>
        </CardHeader>
        <CardContent style={styles.cardContent}>
          <ResponsiveContainer width="100%" height={450}>
            <AreaChart data={product_mix_trend}>
              <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
              <XAxis dataKey="period" tick={{ fontSize: 13, fill: '#374151' }} />
              <YAxis tick={{ fontSize: 13, fill: '#374151' }} />
              <Tooltip contentStyle={{ fontSize: '14px' }} />
              <Legend wrapperStyle={{ fontSize: '13px', paddingTop: '10px' }} />
              {product_mix_trend.length > 0 && Object.keys(product_mix_trend[0])
                .filter(key => key !== 'period')
                .map((product, index) => (
                  <Area
                    key={product}
                    type="monotone"
                    dataKey={product}
                    stackId="1"
                    stroke={COLORS[index % COLORS.length]}
                    fill={COLORS[index % COLORS.length]}
                    name={product}
                  />
                ))
              }
            </AreaChart>
          </ResponsiveContainer>
        </CardContent>
      </Card>

      {/* Top Product-Customer Combinations */}
      <Card style={styles.tableCard}>
        <CardHeader style={styles.cardHeader}>
          <CardTitle style={styles.cardTitle}>Top Product-Customer Combinations</CardTitle>
        </CardHeader>
        <CardContent style={styles.cardContent}>
          <div style={styles.tableWrapper}>
            <table style={styles.table}>
              <thead>
                <tr style={styles.tableHeaderRow}>
                  <th style={styles.tableHeader}>Customer</th>
                  <th style={styles.tableHeader}>Product</th>
                  <th style={{ ...styles.tableHeader, textAlign: 'right' }}>Quote Count</th>
                  <th style={{ ...styles.tableHeader, textAlign: 'right' }}>Revenue</th>
                </tr>
              </thead>
              <tbody>
                {top_combinations.slice(0, 15).map((combo, index) => (
                  <tr key={index} style={styles.tableRow}>
                    <td style={styles.tableCell}>{combo.customer}</td>
                    <td style={styles.tableCell}>{combo.product}</td>
                    <td style={{ ...styles.tableCell, textAlign: 'right' }}>{combo.quote_count}</td>
                    <td style={{ ...styles.tableCell, textAlign: 'right' }}>${combo.revenue.toLocaleString()}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </CardContent>
      </Card>

      {/* Product × Customer Matrix Heatmap */}
      <Card style={styles.fullWidthCard}>
        <CardHeader style={styles.cardHeader}>
          <CardTitle style={styles.cardTitle}>Product × Customer Matrix</CardTitle>
          <p style={styles.cardSubtitle}>
            Shows quote count by product and customer combination
          </p>
        </CardHeader>
        <CardContent style={styles.cardContent}>
          {product_customer_matrix.customers && product_customer_matrix.products && (
            <div style={styles.matrixWrapper}>
              <table style={styles.matrixTable}>
                <thead>
                  <tr>
                    <th style={styles.matrixHeaderCell}>Customer</th>
                    {product_customer_matrix.products.map((product, index) => (
                      <th key={index} style={styles.matrixHeaderCell}>
                        {product}
                      </th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {product_customer_matrix.customers.slice(0, 10).map((customer, idx) => (
                    <tr key={idx}>
                      <td style={styles.matrixRowHeader}>
                        {customer}
                      </td>
                      {product_customer_matrix.products.map((product, pidx) => {
                        const value = product_customer_matrix.data[customer]?.[product] || 0;
                        const intensity = value > 0 ? Math.min(value * 20, 100) : 0;
                        
                        return (
                          <td
                            key={pidx}
                            style={{
                              ...styles.matrixCell,
                              backgroundColor: value > 0 
                                ? `rgba(139, 92, 246, ${intensity / 100})`
                                : 'white'
                            }}
                          >
                            {value || '-'}
                          </td>
                        );
                      })}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </CardContent>
      </Card>

      {/* Funnel Details */}
      <Card style={styles.fullWidthCard}>
        <CardHeader style={styles.cardHeader}>
          <CardTitle style={styles.cardTitle}>Funnel Conversion Details</CardTitle>
        </CardHeader>
        <CardContent style={styles.cardContent}>
          <div style={styles.funnelContainer}>
            {funnel.map((stage, index) => {
              const nextStage = funnel[index + 1];
              const conversionRate = nextStage 
                ? ((nextStage.count / stage.count) * 100).toFixed(1)
                : null;

              return (
                <div key={index} style={styles.funnelItem}>
                  <div style={styles.funnelItemContent}>
                    <h4 style={styles.funnelStageTitle}>{stage.stage}</h4>
                    <p style={styles.funnelStageDetails}>
                      {stage.count} quotes • ${stage.value.toLocaleString()} value
                    </p>
                  </div>
                  {conversionRate && (
                    <div style={styles.funnelConversion}>
                      <p style={styles.funnelConversionRate}>
                        {conversionRate}%
                      </p>
                      <p style={styles.funnelConversionText}>
                        → {nextStage.stage}
                      </p>
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        </CardContent>
      </Card>
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
  metricsCard: {
    marginBottom: '28px',
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
  cardSubtitle: {
    fontSize: '14px',
    color: '#6b7280',
    marginTop: '6px',
  },
  cardContent: {
    padding: '20px',
  },
  metricsGrid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))',
    gap: '20px',
  },
  metricBox: {
    padding: '20px',
    borderRadius: '10px',
  },
  metricBlue: {
    backgroundColor: '#eff6ff',
  },
  metricGreen: {
    backgroundColor: '#f0fdf4',
  },
  metricPurple: {
    backgroundColor: '#faf5ff',
  },
  metricLabel: {
    fontSize: '14px',
    color: '#6b7280',
    marginBottom: '10px',
  },
  metricValue: {
    fontSize: '28px',
    fontWeight: 'bold',
    color: '#111827',
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
  fullWidthCard: {
    marginBottom: '28px',
    boxShadow: '0 2px 4px rgba(0,0,0,0.08)',
    borderRadius: '12px',
    border: '1px solid #e5e7eb',
  },
  tableCard: {
    marginBottom: '28px',
    boxShadow: '0 2px 4px rgba(0,0,0,0.08)',
    borderRadius: '12px',
    border: '1px solid #e5e7eb',
  },
  tableWrapper: {
    overflowX: 'auto',
    maxHeight: '450px',
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
  matrixWrapper: {
    overflowX: 'auto',
    maxHeight: '550px',
    overflowY: 'auto',
  },
  matrixTable: {
    width: '100%',
    borderCollapse: 'collapse',
    fontSize: '13px',
  },
  matrixHeaderCell: {
    border: '1px solid #e5e7eb',
    padding: '12px',
    backgroundColor: '#f9fafb',
    position: 'sticky',
    top: 0,
    zIndex: 2,
    fontSize: '13px',
    fontWeight: '600',
    color: '#374151',
  },
  matrixRowHeader: {
    border: '1px solid #e5e7eb',
    padding: '12px',
    fontWeight: '500',
    backgroundColor: '#f9fafb',
    position: 'sticky',
    left: 0,
    zIndex: 1,
    fontSize: '13px',
  },
  matrixCell: {
    border: '1px solid #e5e7eb',
    padding: '12px',
    textAlign: 'center',
    fontSize: '13px',
  },
  funnelContainer: {
    display: 'flex',
    flexDirection: 'column',
    gap: '16px',
  },
  funnelItem: {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'space-between',
    padding: '20px',
    backgroundColor: '#f9fafb',
    borderRadius: '10px',
    border: '1px solid #e5e7eb',
  },
  funnelItemContent: {
    flex: 1,
  },
  funnelStageTitle: {
    fontWeight: '600',  
    color: '#111827',
    fontSize: '16px',
    margin: 0,
    marginBottom: '6px',
  },
  funnelStageDetails: {
    fontSize: '14px',
    color: '#6b7280',
    margin: 0,
  },
  funnelConversion: {
    marginLeft: '20px',
    textAlign: 'right',
  },
  funnelConversionRate: {
    fontSize: '16px',
    fontWeight: '600',
    color: '#111827',
    margin: 0,
    marginBottom: '4px',
  },
  funnelConversionText: {
    fontSize: '13px',
    color: '#6b7280',
    margin: 0,
  },
};

export default CombinedInsights;
























// import React from 'react';
// import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
// import { Button } from '@/components/ui/button';
// import { useCombinedInsights, exportAnalyticsData } from './hooks/useAnalyticsData.js';
// import {
//   BarChart, Bar, LineChart, Line, AreaChart, Area,
//   XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, Cell
// } from 'recharts';
// import { Download, TrendingUp, Filter } from 'lucide-react';
// import { Loader2 } from 'lucide-react';

// const COLORS = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#ec4899', '#14b8a6', '#f97316', '#06b6d4', '#84cc16'];

// const CombinedInsights = ({ filters }) => {
//   const { data, loading, error } = useCombinedInsights(filters);

//   const handleExport = async (format) => {
//     const result = await exportAnalyticsData('combined', format, filters);
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
//         <span style={styles.loadingText}>Loading combined insights...</span>
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
//     product_customer_matrix, 
//     top_combinations, 
//     funnel, 
//     velocity, 
//     avg_processing_time,
//     product_mix_trend 
//   } = data;

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

//       {/* Key Metrics Card */}
//       <Card style={styles.metricsCard}>
//         <CardHeader style={styles.cardHeader}>
//           <CardTitle style={styles.cardTitle}>Key Insights</CardTitle>
//         </CardHeader>
//         <CardContent style={styles.cardContent}>
//           <div style={styles.metricsGrid}>
//             <div style={{ ...styles.metricBox, ...styles.metricBlue }}>
//               <p style={styles.metricLabel}>Avg Processing Time</p>
//               <p style={styles.metricValue}>
//                 {avg_processing_time ? `${avg_processing_time.toFixed(1)} hrs` : 'N/A'}
//               </p>
//             </div>
//             <div style={{ ...styles.metricBox, ...styles.metricGreen }}>
//               <p style={styles.metricLabel}>Total Product-Customer Combos</p>
//               <p style={styles.metricValue}>
//                 {top_combinations.length}
//               </p>
//             </div>
//             <div style={{ ...styles.metricBox, ...styles.metricPurple }}>
//               <p style={styles.metricLabel}>Active Products</p>
//               <p style={styles.metricValue}>
//                 {product_customer_matrix.products?.length || 0}
//               </p>
//             </div>
//           </div>
//         </CardContent>
//       </Card>

//       {/* Charts Row 1 */}
//       <div style={styles.chartsRow}>
//         {/* Quote Status Funnel */}
//         <Card style={styles.chartCard}>
//           <CardHeader style={styles.cardHeader}>
//             <CardTitle style={styles.cardTitle}>Quote Status Funnel</CardTitle>
//           </CardHeader>
//           <CardContent style={styles.cardContent}>
//             <ResponsiveContainer width="100%" height={400}>
//               <BarChart data={funnel} layout="horizontal">
//                 <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
//                 <XAxis type="number" tick={{ fontSize: 13, fill: '#374151' }} />
//                 <YAxis dataKey="stage" type="category" width={120} tick={{ fontSize: 13, fill: '#374151' }} />
//                 <Tooltip contentStyle={{ fontSize: '14px' }} />
//                 <Legend wrapperStyle={{ fontSize: '14px', paddingTop: '10px' }} />
//                 <Bar dataKey="count" fill="#3b82f6" name="Quote Count" radius={[0, 6, 6, 0]} />
//               </BarChart>
//             </ResponsiveContainer>
//           </CardContent>
//         </Card>

//         {/* Monthly Quote Velocity */}
//         <Card style={styles.chartCard}>
//           <CardHeader style={styles.cardHeader}>
//             <CardTitle style={styles.cardTitle}>Monthly Quote Velocity</CardTitle>
//           </CardHeader>
//           <CardContent style={styles.cardContent}>
//             <ResponsiveContainer width="100%" height={400}>
//               <LineChart data={velocity}>
//                 <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
//                 <XAxis dataKey="date" tick={{ fontSize: 13, fill: '#374151' }} />
//                 <YAxis tick={{ fontSize: 13, fill: '#374151' }} />
//                 <Tooltip contentStyle={{ fontSize: '14px' }} />
//                 <Legend wrapperStyle={{ fontSize: '14px', paddingTop: '10px' }} />
//                 <Line 
//                   type="monotone" 
//                   dataKey="value" 
//                   stroke="#10b981" 
//                   strokeWidth={3}
//                   name="Quotes Created"
//                   dot={{ r: 5, fill: '#10b981' }}
//                   activeDot={{ r: 7 }}
//                 />
//               </LineChart>
//             </ResponsiveContainer>
//           </CardContent>
//         </Card>
//       </div>

//       {/* Product Mix Trend */}
//       <Card style={styles.fullWidthCard}>
//         <CardHeader style={styles.cardHeader}>
//           <CardTitle style={styles.cardTitle}>Product Mix Trend Over Time</CardTitle>
//         </CardHeader>
//         <CardContent style={styles.cardContent}>
//           <ResponsiveContainer width="100%" height={450}>
//             <AreaChart data={product_mix_trend}>
//               <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
//               <XAxis dataKey="period" tick={{ fontSize: 13, fill: '#374151' }} />
//               <YAxis tick={{ fontSize: 13, fill: '#374151' }} />
//               <Tooltip contentStyle={{ fontSize: '14px' }} />
//               <Legend wrapperStyle={{ fontSize: '13px', paddingTop: '10px' }} />
//               {product_mix_trend.length > 0 && Object.keys(product_mix_trend[0])
//                 .filter(key => key !== 'period')
//                 .map((product, index) => (
//                   <Area
//                     key={product}
//                     type="monotone"
//                     dataKey={product}
//                     stackId="1"
//                     stroke={COLORS[index % COLORS.length]}
//                     fill={COLORS[index % COLORS.length]}
//                     name={product}
//                   />
//                 ))
//               }
//             </AreaChart>
//           </ResponsiveContainer>
//         </CardContent>
//       </Card>

//       {/* Top Product-Customer Combinations */}
//       <Card style={styles.tableCard}>
//         <CardHeader style={styles.cardHeader}>
//           <CardTitle style={styles.cardTitle}>Top Product-Customer Combinations</CardTitle>
//         </CardHeader>
//         <CardContent style={styles.cardContent}>
//           <div style={styles.tableWrapper}>
//             <table style={styles.table}>
//               <thead>
//                 <tr style={styles.tableHeaderRow}>
//                   <th style={styles.tableHeader}>Customer</th>
//                   <th style={styles.tableHeader}>Product</th>
//                   <th style={{ ...styles.tableHeader, textAlign: 'right' }}>Quote Count</th>
//                   <th style={{ ...styles.tableHeader, textAlign: 'right' }}>Revenue</th>
//                 </tr>
//               </thead>
//               <tbody>
//                 {top_combinations.slice(0, 15).map((combo, index) => (
//                   <tr key={index} style={styles.tableRow}>
//                     <td style={styles.tableCell}>{combo.customer}</td>
//                     <td style={styles.tableCell}>{combo.product}</td>
//                     <td style={{ ...styles.tableCell, textAlign: 'right' }}>{combo.quote_count}</td>
//                     <td style={{ ...styles.tableCell, textAlign: 'right' }}>${combo.revenue.toLocaleString()}</td>
//                   </tr>
//                 ))}
//               </tbody>
//             </table>
//           </div>
//         </CardContent>
//       </Card>

//       {/* Product × Customer Matrix Heatmap */}
//       <Card style={styles.fullWidthCard}>
//         <CardHeader style={styles.cardHeader}>
//           <CardTitle style={styles.cardTitle}>Product × Customer Matrix</CardTitle>
//           <p style={styles.cardSubtitle}>
//             Shows quote count by product and customer combination
//           </p>
//         </CardHeader>
//         <CardContent style={styles.cardContent}>
//           {product_customer_matrix.customers && product_customer_matrix.products && (
//             <div style={styles.matrixWrapper}>
//               <table style={styles.matrixTable}>
//                 <thead>
//                   <tr>
//                     <th style={styles.matrixHeaderCell}>Customer</th>
//                     {product_customer_matrix.products.map((product, index) => (
//                       <th key={index} style={styles.matrixHeaderCell}>
//                         {product}
//                       </th>
//                     ))}
//                   </tr>
//                 </thead>
//                 <tbody>
//                   {product_customer_matrix.customers.slice(0, 10).map((customer, idx) => (
//                     <tr key={idx}>
//                       <td style={styles.matrixRowHeader}>
//                         {customer}
//                       </td>
//                       {product_customer_matrix.products.map((product, pidx) => {
//                         const value = product_customer_matrix.data[customer]?.[product] || 0;
//                         const intensity = value > 0 ? Math.min(value * 20, 100) : 0;
                        
//                         return (
//                           <td
//                             key={pidx}
//                             style={{
//                               ...styles.matrixCell,
//                               backgroundColor: value > 0 
//                                 ? `rgba(59, 130, 246, ${intensity / 100})`
//                                 : 'white'
//                             }}
//                           >
//                             {value || '-'}
//                           </td>
//                         );
//                       })}
//                     </tr>
//                   ))}
//                 </tbody>
//               </table>
//             </div>
//           )}
//         </CardContent>
//       </Card>

//       {/* Funnel Details */}
//       <Card style={styles.fullWidthCard}>
//         <CardHeader style={styles.cardHeader}>
//           <CardTitle style={styles.cardTitle}>Funnel Conversion Details</CardTitle>
//         </CardHeader>
//         <CardContent style={styles.cardContent}>
//           <div style={styles.funnelContainer}>
//             {funnel.map((stage, index) => {
//               const nextStage = funnel[index + 1];
//               const conversionRate = nextStage 
//                 ? ((nextStage.count / stage.count) * 100).toFixed(1)
//                 : null;

//               return (
//                 <div key={index} style={styles.funnelItem}>
//                   <div style={styles.funnelItemContent}>
//                     <h4 style={styles.funnelStageTitle}>{stage.stage}</h4>
//                     <p style={styles.funnelStageDetails}>
//                       {stage.count} quotes • ${stage.value.toLocaleString()} value
//                     </p>
//                   </div>
//                   {conversionRate && (
//                     <div style={styles.funnelConversion}>
//                       <p style={styles.funnelConversionRate}>
//                         {conversionRate}%
//                       </p>
//                       <p style={styles.funnelConversionText}>
//                         → {nextStage.stage}
//                       </p>
//                     </div>
//                   )}
//                 </div>
//               );
//             })}
//           </div>
//         </CardContent>
//       </Card>
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
//   metricsCard: {
//     marginBottom: '28px',
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
//   cardSubtitle: {
//     fontSize: '14px',
//     color: '#6b7280',
//     marginTop: '6px',
//   },
//   cardContent: {
//     padding: '20px',
//   },
//   metricsGrid: {
//     display: 'grid',
//     gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))',
//     gap: '20px',
//   },
//   metricBox: {
//     padding: '20px',
//     borderRadius: '10px',
//   },
//   metricBlue: {
//     backgroundColor: '#eff6ff',
//   },
//   metricGreen: {
//     backgroundColor: '#f0fdf4',
//   },
//   metricPurple: {
//     backgroundColor: '#faf5ff',
//   },
//   metricLabel: {
//     fontSize: '14px',
//     color: '#6b7280',
//     marginBottom: '10px',
//   },
//   metricValue: {
//     fontSize: '28px',
//     fontWeight: 'bold',
//     color: '#111827',
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
//   fullWidthCard: {
//     marginBottom: '28px',
//     boxShadow: '0 2px 4px rgba(0,0,0,0.08)',
//     borderRadius: '10px',
//     border: '1px solid #e5e7eb',
//   },
//   tableCard: {
//     marginBottom: '28px',
//     boxShadow: '0 2px 4px rgba(0,0,0,0.08)',
//     borderRadius: '10px',
//     border: '1px solid #e5e7eb',
//   },
//   tableWrapper: {
//     overflowX: 'auto',
//     maxHeight: '450px',
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
//   matrixWrapper: {
//     overflowX: 'auto',
//     maxHeight: '550px',
//     overflowY: 'auto',
//   },
//   matrixTable: {
//     width: '100%',
//     borderCollapse: 'collapse',
//     fontSize: '13px',
//   },
//   matrixHeaderCell: {
//     border: '1px solid #e5e7eb',
//     padding: '12px',
//     backgroundColor: '#f9fafb',
//     position: 'sticky',
//     top: 0,
//     zIndex: 2,
//     fontSize: '13px',
//     fontWeight: '600',
//     color: '#374151',
//   },
//   matrixRowHeader: {
//     border: '1px solid #e5e7eb',
//     padding: '12px',
//     fontWeight: '500',
//     backgroundColor: '#f9fafb',
//     position: 'sticky',
//     left: 0,
//     zIndex: 1,
//     fontSize: '13px',
//   },
//   matrixCell: {
//     border: '1px solid #e5e7eb',
//     padding: '12px',
//     textAlign: 'center',
//     fontSize: '13px',
//   },
//   funnelContainer: {
//     display: 'flex',
//     flexDirection: 'column',
//     gap: '16px',
//   },
//   funnelItem: {
//     display: 'flex',
//     alignItems: 'center',
//     justifyContent: 'space-between',
//     padding: '20px',
//     backgroundColor: '#f9fafb',
//     borderRadius: '10px',
//     border: '1px solid #e5e7eb',
//   },
//   funnelItemContent: {
//     flex: 1,
//   },
//   funnelStageTitle: {
//     fontWeight: '600',
//     color: '#111827',
//     fontSize: '16px',
//     margin: 0,
//     marginBottom: '6px',
//   },
//   funnelStageDetails: {
//     fontSize: '14px',
//     color: '#6b7280',
//     margin: 0,
//   },
//   funnelConversion: {
//     marginLeft: '20px',
//     textAlign: 'right',
//   },
//   funnelConversionRate: {
//     fontSize: '16px',
//     fontWeight: '600',
//     color: '#111827',
//     margin: 0,
//     marginBottom: '4px',
//   },
//   funnelConversionText: {
//     fontSize: '13px',
//     color: '#6b7280',
//     margin: 0,
//   },
// };

// export default CombinedInsights;