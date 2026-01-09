import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import KPICard from './components/KPICard';
import ProductFilterPanel from './components/ProductFilterPanel';
import { useProductAnalytics, exportAnalyticsData } from './hooks/useAnalyticsData.js';
import { 
  BarChart, Bar, LineChart, Line, PieChart, Pie, Cell,
  XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer 
} from 'recharts';
import { Download, Package, TrendingUp, DollarSign, Hash } from 'lucide-react';
import { Loader2 } from 'lucide-react';

const COLORS = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#ec4899', '#14b8a6', '#f97316', '#06b6d4', '#84cc16'];

const ProductAnalytics = ({ filters, onFilterChange }) => {
  const { data, loading, error } = useProductAnalytics(filters);

  const handleExport = async (format) => {
    const result = await exportAnalyticsData('product', format, filters);
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
        <span style={styles.loadingText}>Loading analytics...</span>
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

  const { kpis, quote_distribution, revenue_contribution, product_trend, status_breakdown } = data;

  const renderCustomLabel = (entry) => {
    return `${entry.percentage.toFixed(1)}%`;
  };

  return (
    <div style={styles.container}>
      {/* Tab-Specific Filter Panel */}
      <ProductFilterPanel filters={filters} onFilterChange={onFilterChange} />

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
          label={kpis.total_quotes.label}
          value={kpis.total_quotes.value}
          changePercent={kpis.total_quotes.change_percent}
          changeDirection={kpis.total_quotes.change_direction}
          formatType={kpis.total_quotes.format_type}
          icon={Hash}
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
          label={kpis.avg_quote_value.label}
          value={kpis.avg_quote_value.value}
          changePercent={kpis.avg_quote_value.change_percent}
          changeDirection={kpis.avg_quote_value.change_direction}
          formatType={kpis.avg_quote_value.format_type}
          icon={TrendingUp}
        />
        <KPICard
          label={kpis.most_quoted_product.label}
          value={kpis.most_quoted_product.value}
          formatType="text"
          icon={Package}
        />
        <KPICard
          label={kpis.product_count.label}
          value={kpis.product_count.value}
          formatType={kpis.product_count.format_type}
          icon={Package}
        />
      </div>

      {/* Charts Row 1 */}
      <div style={styles.chartsRow}>
        {/* Product Quote Distribution */}
        <Card style={styles.chartCard}>
          <CardHeader style={styles.cardHeader}>
            <CardTitle style={styles.cardTitle}>Quote Distribution by Product</CardTitle>
          </CardHeader>
          <CardContent style={styles.cardContent}>
            <div style={styles.chartWithLegend}>
              <div style={styles.chartWrapper}>
                <ResponsiveContainer width="100%" height={400}>
                  <BarChart data={quote_distribution} layout="vertical">
                    <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
                    <XAxis type="number" tick={{ fontSize: 13, fill: '#374151' }} />
                    <YAxis 
                      dataKey="product_type" 
                      type="category" 
                      width={0}
                      tick={false}
                    />
                    <Tooltip 
                      contentStyle={{ fontSize: '14px', borderRadius: '8px', border: '1px solid #e5e7eb' }}
                      cursor={{ fill: 'rgba(59, 130, 246, 0.1)' }}
                    />
                    <Bar dataKey="quote_count" fill="#3b82f6" name="Quote Count" radius={[0, 6, 6, 0]} />
                  </BarChart>
                </ResponsiveContainer>
              </div>
              
              <div style={styles.productLegend}>
                <div style={styles.legendTitle}>Products</div>
                <div style={styles.legendList}>
                  {quote_distribution.map((item, index) => (
                    <div key={index} style={styles.legendItem}>
                      <div style={{ ...styles.legendColor, backgroundColor: '#3b82f6' }}></div>
                      <span style={styles.legendText}>{item.product_type}</span>
                      <span style={styles.legendValue}>{item.quote_count}</span>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Revenue Contribution */}
        <Card style={styles.chartCard}>
          <CardHeader style={styles.cardHeader}>
            <CardTitle style={styles.cardTitle}>Revenue Contribution by Product</CardTitle>
          </CardHeader>
          <CardContent style={styles.cardContent}>
            <div style={styles.chartWithLegend}>
              <div style={styles.pieChartWrapper}>
                <ResponsiveContainer width="100%" height={400}>
                  <PieChart>
                    <Pie
                      data={revenue_contribution}
                      dataKey="revenue"
                      nameKey="product_type"
                      cx="50%"
                      cy="50%"
                      outerRadius={100}
                      label={renderCustomLabel}
                      labelLine={false}
                    >
                      {revenue_contribution.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                      ))}
                    </Pie>
                    <Tooltip 
                      formatter={(value) => `$${value.toLocaleString()}`}
                      contentStyle={{ fontSize: '14px', borderRadius: '8px', border: '1px solid #e5e7eb' }}
                    />
                  </PieChart>
                </ResponsiveContainer>
              </div>
              
              <div style={styles.productLegend}>
                <div style={styles.legendTitle}>Revenue Breakdown</div>
                <div style={styles.legendList}>
                  {revenue_contribution.map((item, index) => (
                    <div key={index} style={styles.legendItem}>
                      <div style={{ ...styles.legendColor, backgroundColor: COLORS[index % COLORS.length] }}></div>
                      <span style={styles.legendText}>{item.product_type}</span>
                      <span style={styles.legendValue}>${item.revenue.toLocaleString()}</span>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Charts Row 2 */}
      <div style={styles.chartsRow}>
        {/* Product Trend Over Time */}
        <Card style={styles.chartCard}>
          <CardHeader style={styles.cardHeader}>
            <CardTitle style={styles.cardTitle}>Product Quotes Trend Over Time</CardTitle>
          </CardHeader>
          <CardContent style={styles.cardContent}>
            <ResponsiveContainer width="100%" height={400}>
              <LineChart data={product_trend}>
                <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
                <XAxis dataKey="period" tick={{ fontSize: 13, fill: '#374151' }} />
                <YAxis tick={{ fontSize: 13, fill: '#374151' }} />
                <Tooltip 
                  contentStyle={{ fontSize: '14px', borderRadius: '8px', border: '1px solid #e5e7eb' }}
                />
                <Legend wrapperStyle={{ fontSize: '13px', paddingTop: '10px' }} />
                {product_trend.length > 0 && Object.keys(product_trend[0])
                  .filter(key => key !== 'period')
                  .slice(0, 5)
                  .map((product, index) => (
                    <Line 
                      key={product}
                      type="monotone" 
                      dataKey={product} 
                      stroke={COLORS[index % COLORS.length]} 
                      name={product}
                      strokeWidth={2.5}
                      dot={{ r: 4 }}
                    />
                  ))
                }
              </LineChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        {/* Product by Status Breakdown */}
        <Card style={styles.chartCard}>
          <CardHeader style={styles.cardHeader}>
            <CardTitle style={styles.cardTitle}>Product Quotes by Status</CardTitle>
          </CardHeader>
          <CardContent style={styles.cardContent}>
            <div style={styles.chartWithLegend}>
              <div style={styles.chartWrapper}>
                <ResponsiveContainer width="100%" height={400}>
                  <BarChart data={status_breakdown} layout="vertical">
                    <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
                    <XAxis type="number" tick={{ fontSize: 13, fill: '#374151' }} />
                    <YAxis 
                      dataKey="product_type" 
                      type="category" 
                      width={0}
                      tick={false}
                    />
                    <Tooltip 
                      contentStyle={{ fontSize: '14px', borderRadius: '8px', border: '1px solid #e5e7eb' }}
                    />
                    <Legend wrapperStyle={{ fontSize: '13px', paddingTop: '10px' }} />
                    <Bar dataKey="Budgetary" stackId="a" fill="#fbbf24" name="Budgetary" />
                    <Bar dataKey="Active" stackId="a" fill="#3b82f6" name="Active" />
                    <Bar dataKey="Won" stackId="a" fill="#10b981" name="Won" />
                    <Bar dataKey="Lost" stackId="a" fill="#ef4444" name="Lost" />
                  </BarChart>
                </ResponsiveContainer>
              </div>
              
              <div style={styles.productLegend}>
                <div style={styles.legendTitle}>Products</div>
                <div style={styles.legendList}>
                  {status_breakdown.map((item, index) => (
                    <div key={index} style={styles.legendItem}>
                      <div style={{ ...styles.legendColor, backgroundColor: '#6b7280' }}></div>
                      <span style={styles.legendText}>{item.product_type}</span>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Data Table */}
      <Card style={styles.tableCard}>
        <CardHeader style={styles.cardHeader}>
          <CardTitle style={styles.cardTitle}>Detailed Product Performance</CardTitle>
        </CardHeader>
        <CardContent style={styles.cardContent}>
          <div style={styles.tableWrapper}>
            <table style={styles.table}>
              <thead>
                <tr style={styles.tableHeaderRow}>
                  <th style={styles.tableHeader}>Product Type</th>
                  <th style={{ ...styles.tableHeader, textAlign: 'right' }}>Quote Count</th>
                  <th style={{ ...styles.tableHeader, textAlign: 'right' }}>Revenue</th>
                  <th style={{ ...styles.tableHeader, textAlign: 'right' }}>Avg Value</th>
                  <th style={{ ...styles.tableHeader, textAlign: 'right' }}>% of Total</th>
                </tr>
              </thead>
              <tbody>
                {revenue_contribution.map((product, index) => (
                  <tr key={index} style={styles.tableRow}>
                    <td style={styles.tableCell}>
                      <div style={styles.tableCellWithColor}>
                        <div style={{ ...styles.tableColorDot, backgroundColor: COLORS[index % COLORS.length] }}></div>
                        {product.product_type}
                      </div>
                    </td>
                    <td style={{ ...styles.tableCell, textAlign: 'right' }}>{product.quote_count}</td>
                    <td style={{ ...styles.tableCell, textAlign: 'right' }}>${product.revenue.toLocaleString()}</td>
                    <td style={{ ...styles.tableCell, textAlign: 'right' }}>${product.avg_value.toLocaleString()}</td>
                    <td style={{ ...styles.tableCell, textAlign: 'right' }}>{product.percentage.toFixed(2)}%</td>
                  </tr>
                ))}
              </tbody>
            </table>
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
  kpiGrid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))',
    gap: '18px',
    marginBottom: '28px',
  },
  chartsRow: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(650px, 1fr))',
    gap: '24px',
    marginBottom: '28px',
  },
  chartCard: {
    boxShadow: '0 1px 3px rgba(0,0,0,0.08)',
    borderRadius: '12px',
    border: '1px solid #e5e7eb',
    backgroundColor: '#ffffff',
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
  chartWithLegend: {
    display: 'flex',
    gap: '20px',
    alignItems: 'flex-start',
  },
  chartWrapper: {
    flex: '1 1 70%',
    minWidth: '400px',
  },
  pieChartWrapper: {
    flex: '1 1 60%',
    minWidth: '350px',
  },
  productLegend: {
    flex: '1 1 30%',
    minWidth: '200px',
    maxWidth: '300px',
  },
  legendTitle: {
    fontSize: '14px',
    fontWeight: '600',
    color: '#111827',
    marginBottom: '12px',
    paddingBottom: '8px',
    borderBottom: '2px solid #f3f4f6',
  },
  legendList: {
    maxHeight: '350px',
    overflowY: 'auto',
    overflowX: 'hidden',
    paddingRight: '8px',
  },
  legendItem: {
    display: 'flex',
    alignItems: 'center',
    gap: '8px',
    padding: '8px',
    marginBottom: '4px',
    borderRadius: '6px',
    transition: 'background-color 0.2s',
    cursor: 'default',
  },
  legendColor: {
    width: '12px',
    height: '12px',
    borderRadius: '3px',
    flexShrink: 0,
  },
  legendText: {
    flex: 1,
    fontSize: '13px',
    color: '#374151',
    overflow: 'hidden',
    textOverflow: 'ellipsis',
    whiteSpace: 'nowrap',
  },
  legendValue: {
    fontSize: '13px',
    fontWeight: '600',
    color: '#111827',
    flexShrink: 0,
  },
  tableCard: {
    marginTop: '28px',
    boxShadow: '0 1px 3px rgba(0,0,0,0.08)',
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
    borderBottom: '1px solid #f3f4f6',
  },
  tableCell: {
    padding: '14px',
    color: '#1f2937',
    fontSize: '14px',
  },
  tableCellWithColor: {
    display: 'flex',
    alignItems: 'center',
    gap: '8px',
  },
  tableColorDot: {
    width: '10px',
    height: '10px',
    borderRadius: '50%',
    flexShrink: 0,
  },
};

export default ProductAnalytics;



































// import React from 'react';
// import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
// import { Button } from '@/components/ui/button';
// import KPICard from './components/KPICard';
// import { useProductAnalytics, exportAnalyticsData } from './hooks/useAnalyticsData.js';
// import { 
//   BarChart, Bar, LineChart, Line, PieChart, Pie, Cell,
//   XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer 
// } from 'recharts';
// import { Download, Package, TrendingUp, DollarSign, Hash } from 'lucide-react';
// import { Loader2 } from 'lucide-react';

// const COLORS = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#ec4899', '#14b8a6', '#f97316', '#06b6d4', '#84cc16'];

// const ProductAnalytics = ({ filters }) => {
//   const { data, loading, error } = useProductAnalytics(filters);

//   const handleExport = async (format) => {
//     const result = await exportAnalyticsData('product', format, filters);
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
//         <span style={styles.loadingText}>Loading analytics...</span>
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

//   const { kpis, quote_distribution, revenue_contribution, product_trend, status_breakdown } = data;

//   // Custom label for pie chart with product names
//   const renderCustomLabel = (entry) => {
//     return `${entry.percentage.toFixed(1)}%`;
//   };

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
//           label={kpis.total_quotes.label}
//           value={kpis.total_quotes.value}
//           changePercent={kpis.total_quotes.change_percent}
//           changeDirection={kpis.total_quotes.change_direction}
//           formatType={kpis.total_quotes.format_type}
//           icon={Hash}
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
//           label={kpis.avg_quote_value.label}
//           value={kpis.avg_quote_value.value}
//           changePercent={kpis.avg_quote_value.change_percent}
//           changeDirection={kpis.avg_quote_value.change_direction}
//           formatType={kpis.avg_quote_value.format_type}
//           icon={TrendingUp}
//         />
//         <KPICard
//           label={kpis.most_quoted_product.label}
//           value={kpis.most_quoted_product.value}
//           formatType="text"
//           icon={Package}
//         />
//         <KPICard
//           label={kpis.product_count.label}
//           value={kpis.product_count.value}
//           formatType={kpis.product_count.format_type}
//           icon={Package}
//         />
//       </div>

//       {/* Charts Row 1 */}
//       <div style={styles.chartsRow}>
//         {/* Product Quote Distribution - VERTICAL BARS with scrollable list */}
//         <Card style={styles.chartCard}>
//           <CardHeader style={styles.cardHeader}>
//             <CardTitle style={styles.cardTitle}>Quote Distribution by Product</CardTitle>
//           </CardHeader>
//           <CardContent style={styles.cardContent}>
//             <div style={styles.chartWithLegend}>
//               {/* Chart */}
//               <div style={styles.chartWrapper}>
//                 <ResponsiveContainer width="100%" height={400}>
//                   <BarChart data={quote_distribution} layout="vertical">
//                     <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
//                     <XAxis type="number" tick={{ fontSize: 13, fill: '#374151' }} />
//                     <YAxis 
//                       dataKey="product_type" 
//                       type="category" 
//                       width={0}
//                       tick={false}
//                     />
//                     <Tooltip 
//                       contentStyle={{ fontSize: '14px', borderRadius: '8px', border: '1px solid #e5e7eb' }}
//                       cursor={{ fill: 'rgba(59, 130, 246, 0.1)' }}
//                     />
//                     <Bar dataKey="quote_count" fill="#3b82f6" name="Quote Count" radius={[0, 6, 6, 0]} />
//                   </BarChart>
//                 </ResponsiveContainer>
//               </div>
              
//               {/* Product Legend */}
//               <div style={styles.productLegend}>
//                 <div style={styles.legendTitle}>Products</div>
//                 <div style={styles.legendList}>
//                   {quote_distribution.map((item, index) => (
//                     <div key={index} style={styles.legendItem}>
//                       <div style={{ ...styles.legendColor, backgroundColor: '#3b82f6' }}></div>
//                       <span style={styles.legendText}>{item.product_type}</span>
//                       <span style={styles.legendValue}>{item.quote_count}</span>
//                     </div>
//                   ))}
//                 </div>
//               </div>
//             </div>
//           </CardContent>
//         </Card>

//         {/* Revenue Contribution - PIE CHART with external legend */}
//         <Card style={styles.chartCard}>
//           <CardHeader style={styles.cardHeader}>
//             <CardTitle style={styles.cardTitle}>Revenue Contribution by Product</CardTitle>
//           </CardHeader>
//           <CardContent style={styles.cardContent}>
//             <div style={styles.chartWithLegend}>
//               {/* Pie Chart */}
//               <div style={styles.pieChartWrapper}>
//                 <ResponsiveContainer width="100%" height={400}>
//                   <PieChart>
//                     <Pie
//                       data={revenue_contribution}
//                       dataKey="revenue"
//                       nameKey="product_type"
//                       cx="50%"
//                       cy="50%"
//                       outerRadius={100}
//                       label={renderCustomLabel}
//                       labelLine={false}
//                     >
//                       {revenue_contribution.map((entry, index) => (
//                         <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
//                       ))}
//                     </Pie>
//                     <Tooltip 
//                       formatter={(value) => `$${value.toLocaleString()}`}
//                       contentStyle={{ fontSize: '14px', borderRadius: '8px', border: '1px solid #e5e7eb' }}
//                     />
//                   </PieChart>
//                 </ResponsiveContainer>
//               </div>
              
//               {/* Revenue Legend */}
//               <div style={styles.productLegend}>
//                 <div style={styles.legendTitle}>Revenue Breakdown</div>
//                 <div style={styles.legendList}>
//                   {revenue_contribution.map((item, index) => (
//                     <div key={index} style={styles.legendItem}>
//                       <div style={{ ...styles.legendColor, backgroundColor: COLORS[index % COLORS.length] }}></div>
//                       <span style={styles.legendText}>{item.product_type}</span>
//                       <span style={styles.legendValue}>${item.revenue.toLocaleString()}</span>
//                     </div>
//                   ))}
//                 </div>
//               </div>
//             </div>
//           </CardContent>
//         </Card>
//       </div>

//       {/* Charts Row 2 */}
//       <div style={styles.chartsRow}>
//         {/* Product Trend Over Time */}
//         <Card style={styles.chartCard}>
//           <CardHeader style={styles.cardHeader}>
//             <CardTitle style={styles.cardTitle}>Product Quotes Trend Over Time</CardTitle>
//           </CardHeader>
//           <CardContent style={styles.cardContent}>
//             <ResponsiveContainer width="100%" height={400}>
//               <LineChart data={product_trend}>
//                 <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
//                 <XAxis dataKey="period" tick={{ fontSize: 13, fill: '#374151' }} />
//                 <YAxis tick={{ fontSize: 13, fill: '#374151' }} />
//                 <Tooltip 
//                   contentStyle={{ fontSize: '14px', borderRadius: '8px', border: '1px solid #e5e7eb' }}
//                 />
//                 <Legend wrapperStyle={{ fontSize: '13px', paddingTop: '10px' }} />
//                 {product_trend.length > 0 && Object.keys(product_trend[0])
//                   .filter(key => key !== 'period')
//                   .slice(0, 5)  // Show only top 5 products in line chart
//                   .map((product, index) => (
//                     <Line 
//                       key={product}
//                       type="monotone" 
//                       dataKey={product} 
//                       stroke={COLORS[index % COLORS.length]} 
//                       name={product}
//                       strokeWidth={2.5}
//                       dot={{ r: 4 }}
//                     />
//                   ))
//                 }
//               </LineChart>
//             </ResponsiveContainer>
//           </CardContent>
//         </Card>

//         {/* Product by Status Breakdown */}
//         <Card style={styles.chartCard}>
//           <CardHeader style={styles.cardHeader}>
//             <CardTitle style={styles.cardTitle}>Product Quotes by Status</CardTitle>
//           </CardHeader>
//           <CardContent style={styles.cardContent}>
//             <div style={styles.chartWithLegend}>
//               {/* Chart */}
//               <div style={styles.chartWrapper}>
//                 <ResponsiveContainer width="100%" height={400}>
//                   <BarChart data={status_breakdown} layout="vertical">
//                     <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
//                     <XAxis type="number" tick={{ fontSize: 13, fill: '#374151' }} />
//                     <YAxis 
//                       dataKey="product_type" 
//                       type="category" 
//                       width={0}
//                       tick={false}
//                     />
//                     <Tooltip 
//                       contentStyle={{ fontSize: '14px', borderRadius: '8px', border: '1px solid #e5e7eb' }}
//                     />
//                     <Legend wrapperStyle={{ fontSize: '13px', paddingTop: '10px' }} />
//                     <Bar dataKey="Budgetary" stackId="a" fill="#fbbf24" name="Budgetary" />
//                     <Bar dataKey="Active" stackId="a" fill="#3b82f6" name="Active" />
//                     <Bar dataKey="Won" stackId="a" fill="#10b981" name="Won" />
//                     <Bar dataKey="Lost" stackId="a" fill="#ef4444" name="Lost" />
//                   </BarChart>
//                 </ResponsiveContainer>
//               </div>
              
//               {/* Product Legend for Status */}
//               <div style={styles.productLegend}>
//                 <div style={styles.legendTitle}>Products</div>
//                 <div style={styles.legendList}>
//                   {status_breakdown.map((item, index) => (
//                     <div key={index} style={styles.legendItem}>
//                       <div style={{ ...styles.legendColor, backgroundColor: '#6b7280' }}></div>
//                       <span style={styles.legendText}>{item.product_type}</span>
//                     </div>
//                   ))}
//                 </div>
//               </div>
//             </div>
//           </CardContent>
//         </Card>
//       </div>

//       {/* Data Table */}
//       <Card style={styles.tableCard}>
//         <CardHeader style={styles.cardHeader}>
//           <CardTitle style={styles.cardTitle}>Detailed Product Performance</CardTitle>
//         </CardHeader>
//         <CardContent style={styles.cardContent}>
//           <div style={styles.tableWrapper}>
//             <table style={styles.table}>
//               <thead>
//                 <tr style={styles.tableHeaderRow}>
//                   <th style={styles.tableHeader}>Product Type</th>
//                   <th style={{ ...styles.tableHeader, textAlign: 'right' }}>Quote Count</th>
//                   <th style={{ ...styles.tableHeader, textAlign: 'right' }}>Revenue</th>
//                   <th style={{ ...styles.tableHeader, textAlign: 'right' }}>Avg Value</th>
//                   <th style={{ ...styles.tableHeader, textAlign: 'right' }}>% of Total</th>
//                 </tr>
//               </thead>
//               <tbody>
//                 {revenue_contribution.map((product, index) => (
//                   <tr key={index} style={styles.tableRow}>
//                     <td style={styles.tableCell}>
//                       <div style={styles.tableCellWithColor}>
//                         <div style={{ ...styles.tableColorDot, backgroundColor: COLORS[index % COLORS.length] }}></div>
//                         {product.product_type}
//                       </div>
//                     </td>
//                     <td style={{ ...styles.tableCell, textAlign: 'right' }}>{product.quote_count}</td>
//                     <td style={{ ...styles.tableCell, textAlign: 'right' }}>${product.revenue.toLocaleString()}</td>
//                     <td style={{ ...styles.tableCell, textAlign: 'right' }}>${product.avg_value.toLocaleString()}</td>
//                     <td style={{ ...styles.tableCell, textAlign: 'right' }}>{product.percentage.toFixed(2)}%</td>
//                   </tr>
//                 ))}
//               </tbody>
//             </table>
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
//     fontWeight: '500',
//     backgroundColor: '#ffffff',
//     color: '#374151',
//     border: '1px solid #d1d5db',
//     borderRadius: '8px',
//     cursor: 'pointer',
//     transition: 'all 0.2s',
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
//     gridTemplateColumns: 'repeat(auto-fit, minmax(650px, 1fr))',
//     gap: '24px',
//     marginBottom: '28px',
//   },
//   chartCard: {
//     boxShadow: '0 1px 3px rgba(0,0,0,0.08)',
//     borderRadius: '12px',
//     border: '1px solid #e5e7eb',
//     backgroundColor: '#ffffff',
//   },
//   cardHeader: {
//     padding: '20px',
//     borderBottom: '2px solid #f3f4f6',
//   },
//   cardTitle: {
//     fontSize: '17px',
//     fontWeight: '600',
//     color: '#111827',
//   },
//   cardContent: {
//     padding: '20px',
//   },
//   chartWithLegend: {
//     display: 'flex',
//     gap: '20px',
//     alignItems: 'flex-start',
//   },
//   chartWrapper: {
//     flex: '1 1 70%',
//     minWidth: '400px',
//   },
//   pieChartWrapper: {
//     flex: '1 1 60%',
//     minWidth: '350px',
//   },
//   productLegend: {
//     flex: '1 1 30%',
//     minWidth: '200px',
//     maxWidth: '300px',
//   },
//   legendTitle: {
//     fontSize: '14px',
//     fontWeight: '600',
//     color: '#111827',
//     marginBottom: '12px',
//     paddingBottom: '8px',
//     borderBottom: '2px solid #f3f4f6',
//   },
//   legendList: {
//     maxHeight: '350px',
//     overflowY: 'auto',
//     overflowX: 'hidden',
//     paddingRight: '8px',
//   },
//   legendItem: {
//     display: 'flex',
//     alignItems: 'center',
//     gap: '8px',
//     padding: '8px',
//     marginBottom: '4px',
//     borderRadius: '6px',
//     transition: 'background-color 0.2s',
//     cursor: 'default',
//   },
//   legendColor: {
//     width: '12px',
//     height: '12px',
//     borderRadius: '3px',
//     flexShrink: 0,
//   },
//   legendText: {
//     flex: 1,
//     fontSize: '13px',
//     color: '#374151',
//     overflow: 'hidden',
//     textOverflow: 'ellipsis',
//     whiteSpace: 'nowrap',
//   },
//   legendValue: {
//     fontSize: '13px',
//     fontWeight: '600',
//     color: '#111827',
//     flexShrink: 0,
//   },
//   tableCard: {
//     marginTop: '28px',
//     boxShadow: '0 1px 3px rgba(0,0,0,0.08)',
//     borderRadius: '12px',
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
//     borderBottom: '1px solid #f3f4f6',
//   },
//   tableCell: {
//     padding: '14px',
//     color: '#1f2937',
//     fontSize: '14px',
//   },
//   tableCellWithColor: {
//     display: 'flex',
//     alignItems: 'center',
//     gap: '8px',
//   },
//   tableColorDot: {
//     width: '10px',
//     height: '10px',
//     borderRadius: '50%',
//     flexShrink: 0,
//   },
// };

// // Add hover effects
// const styleSheet = document.createElement('style');
// styleSheet.textContent = `
//   tr:hover {
//     background-color: #f9fafb !important;
//   }
//   div[style*="legendItem"]:hover {
//     background-color: #f3f4f6 !important;
//   }
// `;
// if (!document.querySelector('style[data-product-analytics]')) {
//   styleSheet.setAttribute('data-product-analytics', '');
//   document.head.appendChild(styleSheet);
// }

// export default ProductAnalytics;









//--------------------------------------------------------------------------------------------------

// import React from 'react';
// import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
// import { Button } from '@/components/ui/button';
// import KPICard from './components/KPICard';
// import { useProductAnalytics, exportAnalyticsData } from './hooks/useAnalyticsData.js';
// import { 
//   BarChart, Bar, LineChart, Line, PieChart, Pie, Cell,
//   XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer 
// } from 'recharts';
// import { Download, Package, TrendingUp, DollarSign, Hash } from 'lucide-react';
// import { Loader2 } from 'lucide-react';

// const COLORS = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#ec4899', '#14b8a6', '#f97316', '#06b6d4', '#84cc16'];

// const ProductAnalytics = ({ filters }) => {
//   const { data, loading, error } = useProductAnalytics(filters);

//   const handleExport = async (format) => {
//     const result = await exportAnalyticsData('product', format, filters);
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
//         <span style={styles.loadingText}>Loading analytics...</span>
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

//   const { kpis, quote_distribution, revenue_contribution, product_trend, status_breakdown } = data;

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
//           label={kpis.total_quotes.label}
//           value={kpis.total_quotes.value}
//           changePercent={kpis.total_quotes.change_percent}
//           changeDirection={kpis.total_quotes.change_direction}
//           formatType={kpis.total_quotes.format_type}
//           icon={Hash}
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
//           label={kpis.avg_quote_value.label}
//           value={kpis.avg_quote_value.value}
//           changePercent={kpis.avg_quote_value.change_percent}
//           changeDirection={kpis.avg_quote_value.change_direction}
//           formatType={kpis.avg_quote_value.format_type}
//           icon={TrendingUp}
//         />
//         <KPICard
//           label={kpis.most_quoted_product.label}
//           value={kpis.most_quoted_product.value}
//           formatType="text"
//           icon={Package}
//         />
//         <KPICard
//           label={kpis.product_count.label}
//           value={kpis.product_count.value}
//           formatType={kpis.product_count.format_type}
//           icon={Package}
//         />
//       </div>

//       {/* Charts Row 1 */}
//       <div style={styles.chartsRow}>
//         {/* Product Quote Distribution - with horizontal scroll */}
//         <Card style={styles.chartCard}>
//           <CardHeader style={styles.cardHeader}>
//             <CardTitle style={styles.cardTitle}>Quote Distribution by Product</CardTitle>
//           </CardHeader>
//           <CardContent style={styles.cardContent}>
//             <div style={styles.chartScrollWrapper}>
//               <div style={{ minWidth: Math.max(800, quote_distribution.length * 60) }}>
//                 <ResponsiveContainer width="100%" height={400}>
//                   <BarChart data={quote_distribution}>
//                     <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
//                     <XAxis 
//                       dataKey="product_type" 
//                       angle={-45}
//                       textAnchor="end"
//                       height={140}
//                       interval={0}
//                       tick={{ fontSize: 12, fill: '#374151' }}
//                     />
//                     <YAxis tick={{ fontSize: 13, fill: '#374151' }} />
//                     <Tooltip contentStyle={{ fontSize: '14px' }} />
//                     <Legend wrapperStyle={{ fontSize: '14px', paddingTop: '10px' }} />
//                     <Bar dataKey="quote_count" fill="#3b82f6" name="Quote Count" radius={[4, 4, 0, 0]} />
//                   </BarChart>
//                 </ResponsiveContainer>
//               </div>
//             </div>
//           </CardContent>
//         </Card>

//         {/* Revenue Contribution */}
//         <Card style={styles.chartCard}>
//           <CardHeader style={styles.cardHeader}>
//             <CardTitle style={styles.cardTitle}>Revenue Contribution by Product</CardTitle>
//           </CardHeader>
//           <CardContent style={styles.cardContent}>
//             <ResponsiveContainer width="100%" height={400}>
//               <PieChart>
//                 <Pie
//                   data={revenue_contribution}
//                   dataKey="revenue"
//                   nameKey="product_type"
//                   cx="50%"
//                   cy="50%"
//                   outerRadius={120}
//                   label={(entry) => `${entry.percentage.toFixed(1)}%`}
//                   labelLine={true}
//                 >
//                   {revenue_contribution.map((entry, index) => (
//                     <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
//                   ))}
//                 </Pie>
//                 <Tooltip formatter={(value) => `$${value.toLocaleString()}`} contentStyle={{ fontSize: '14px' }} />
//                 <Legend wrapperStyle={{ fontSize: '13px' }} />
//               </PieChart>
//             </ResponsiveContainer>
//           </CardContent>
//         </Card>
//       </div>

//       {/* Charts Row 2 */}
//       <div style={styles.chartsRow}>
//         {/* Product Trend Over Time */}
//         <Card style={styles.chartCard}>
//           <CardHeader style={styles.cardHeader}>
//             <CardTitle style={styles.cardTitle}>Product Quotes Trend Over Time</CardTitle>
//           </CardHeader>
//           <CardContent style={styles.cardContent}>
//             <ResponsiveContainer width="100%" height={400}>
//               <LineChart data={product_trend}>
//                 <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
//                 <XAxis dataKey="period" tick={{ fontSize: 13, fill: '#374151' }} />
//                 <YAxis tick={{ fontSize: 13, fill: '#374151' }} />
//                 <Tooltip contentStyle={{ fontSize: '14px' }} />
//                 <Legend wrapperStyle={{ fontSize: '13px', paddingTop: '10px' }} />
//                 {product_trend.length > 0 && Object.keys(product_trend[0])
//                   .filter(key => key !== 'period')
//                   .map((product, index) => (
//                     <Line 
//                       key={product}
//                       type="monotone" 
//                       dataKey={product} 
//                       stroke={COLORS[index % COLORS.length]} 
//                       name={product}
//                       strokeWidth={2.5}
//                       dot={{ r: 4 }}
//                     />
//                   ))
//                 }
//               </LineChart>
//             </ResponsiveContainer>
//           </CardContent>
//         </Card>

//         {/* Product by Status Breakdown - with horizontal scroll */}
//         <Card style={styles.chartCard}>
//           <CardHeader style={styles.cardHeader}>
//             <CardTitle style={styles.cardTitle}>Product Quotes by Status</CardTitle>
//           </CardHeader>
//           <CardContent style={styles.cardContent}>
//             <div style={styles.chartScrollWrapper}>
//               <div style={{ minWidth: Math.max(800, status_breakdown.length * 60) }}>
//                 <ResponsiveContainer width="100%" height={400}>
//                   <BarChart data={status_breakdown}>
//                     <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
//                     <XAxis 
//                       dataKey="product_type"
//                       angle={-45}
//                       textAnchor="end"
//                       height={140}
//                       interval={0}
//                       tick={{ fontSize: 12, fill: '#374151' }}
//                     />
//                     <YAxis tick={{ fontSize: 13, fill: '#374151' }} />
//                     <Tooltip contentStyle={{ fontSize: '14px' }} />
//                     <Legend wrapperStyle={{ fontSize: '13px', paddingTop: '10px' }} />
//                     <Bar dataKey="Budgetary" stackId="a" fill="#fbbf24" name="Budgetary" radius={[0, 0, 0, 0]} />
//                     <Bar dataKey="Active" stackId="a" fill="#3b82f6" name="Active" radius={[0, 0, 0, 0]} />
//                     <Bar dataKey="Won" stackId="a" fill="#10b981" name="Won" radius={[0, 0, 0, 0]} />
//                     <Bar dataKey="Lost" stackId="a" fill="#ef4444" name="Lost" radius={[4, 4, 0, 0]} />
//                   </BarChart>
//                 </ResponsiveContainer>
//               </div>
//             </div>
//           </CardContent>
//         </Card>
//       </div>

//       {/* Data Table */}
//       <Card style={styles.tableCard}>
//         <CardHeader style={styles.cardHeader}>
//           <CardTitle style={styles.cardTitle}>Detailed Product Performance</CardTitle>
//         </CardHeader>
//         <CardContent style={styles.cardContent}>
//           <div style={styles.tableWrapper}>
//             <table style={styles.table}>
//               <thead>
//                 <tr style={styles.tableHeaderRow}>
//                   <th style={styles.tableHeader}>Product Type</th>
//                   <th style={{ ...styles.tableHeader, textAlign: 'right' }}>Quote Count</th>
//                   <th style={{ ...styles.tableHeader, textAlign: 'right' }}>Revenue</th>
//                   <th style={{ ...styles.tableHeader, textAlign: 'right' }}>Avg Value</th>
//                   <th style={{ ...styles.tableHeader, textAlign: 'right' }}>% of Total</th>
//                 </tr>
//               </thead>
//               <tbody>
//                 {revenue_contribution.map((product, index) => (
//                   <tr key={index} style={styles.tableRow}>
//                     <td style={styles.tableCell}>{product.product_type}</td>
//                     <td style={{ ...styles.tableCell, textAlign: 'right' }}>{product.quote_count}</td>
//                     <td style={{ ...styles.tableCell, textAlign: 'right' }}>${product.revenue.toLocaleString()}</td>
//                     <td style={{ ...styles.tableCell, textAlign: 'right' }}>${product.avg_value.toLocaleString()}</td>
//                     <td style={{ ...styles.tableCell, textAlign: 'right' }}>{product.percentage.toFixed(2)}%</td>
//                   </tr>
//                 ))}
//               </tbody>
//             </table>
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
//   tableCard: {
//     marginTop: '28px',
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
// };

// export default ProductAnalytics;









//--------------------------------------------------------------------------------------------------


// import React from 'react';
// import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
// import { Button } from '@/components/ui/button';
// import KPICard from './components/KPICard';
// import { useProductAnalytics, exportAnalyticsData } from './hooks/useAnalyticsData.js';
// import { 
//   BarChart, Bar, LineChart, Line, PieChart, Pie, Cell,
//   XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer 
// } from 'recharts';
// import { Download, Package, TrendingUp, DollarSign, Hash } from 'lucide-react';
// import { Loader2 } from 'lucide-react';

// const COLORS = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6'];

// const ProductAnalytics = ({ filters }) => {
//   const { data, loading, error } = useProductAnalytics(filters);

//   const handleExport = async (format) => {
//     const result = await exportAnalyticsData('product', format, filters);
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
//         <span className="ml-2 text-gray-600">Loading analytics...</span>
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

//   const { kpis, quote_distribution, revenue_contribution, product_trend, status_breakdown } = data;

//   return (
//     <div className="space-y-6">
//       {/* Export Button */}
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
//           label={kpis.total_quotes.label}
//           value={kpis.total_quotes.value}
//           changePercent={kpis.total_quotes.change_percent}
//           changeDirection={kpis.total_quotes.change_direction}
//           formatType={kpis.total_quotes.format_type}
//           icon={Hash}
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
//           label={kpis.avg_quote_value.label}
//           value={kpis.avg_quote_value.value}
//           changePercent={kpis.avg_quote_value.change_percent}
//           changeDirection={kpis.avg_quote_value.change_direction}
//           formatType={kpis.avg_quote_value.format_type}
//           icon={TrendingUp}
//         />
//         <KPICard
//           label={kpis.most_quoted_product.label}
//           value={kpis.most_quoted_product.value}
//           formatType="text"
//           icon={Package}
//         />
//         <KPICard
//           label={kpis.product_count.label}
//           value={kpis.product_count.value}
//           formatType={kpis.product_count.format_type}
//           icon={Package}
//         />
//       </div>

//       {/* Charts Row 1 */}
//       <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
//         {/* Product Quote Distribution */}
//         <Card>
//           <CardHeader>
//             <CardTitle>Quote Distribution by Product</CardTitle>
//           </CardHeader>
//           <CardContent>
//             <ResponsiveContainer width="100%" height={300}>
//               <BarChart data={quote_distribution}>
//                 <CartesianGrid strokeDasharray="3 3" />
//                 <XAxis 
//                   dataKey="product_type" 
//                   angle={-45}
//                   textAnchor="end"
//                   height={100}
//                   interval={0}
//                   tick={{ fontSize: 12 }}
//                 />
//                 <YAxis />
//                 <Tooltip />
//                 <Legend />
//                 <Bar dataKey="quote_count" fill="#3b82f6" name="Quote Count" />
//               </BarChart>
//             </ResponsiveContainer>
//           </CardContent>
//         </Card>

//         {/* Revenue Contribution */}
//         <Card>
//           <CardHeader>
//             <CardTitle>Revenue Contribution by Product</CardTitle>
//           </CardHeader>
//           <CardContent>
//             <ResponsiveContainer width="100%" height={300}>
//               <PieChart>
//                 <Pie
//                   data={revenue_contribution}
//                   dataKey="revenue"
//                   nameKey="product_type"
//                   cx="50%"
//                   cy="50%"
//                   outerRadius={100}
//                   label={(entry) => `${entry.product_type}: ${entry.percentage.toFixed(1)}%`}
//                 >
//                   {revenue_contribution.map((entry, index) => (
//                     <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
//                   ))}
//                 </Pie>
//                 <Tooltip formatter={(value) => `$${value.toLocaleString()}`} />
//               </PieChart>
//             </ResponsiveContainer>
//           </CardContent>
//         </Card>
//       </div>

//       {/* Charts Row 2 */}
//       <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
//         {/* Product Trend Over Time */}
//         <Card>
//           <CardHeader>
//             <CardTitle>Product Quotes Trend Over Time</CardTitle>
//           </CardHeader>
//           <CardContent>
//             <ResponsiveContainer width="100%" height={300}>
//               <LineChart data={product_trend}>
//                 <CartesianGrid strokeDasharray="3 3" />
//                 <XAxis dataKey="period" />
//                 <YAxis />
//                 <Tooltip />
//                 <Legend />
//                 {product_trend.length > 0 && Object.keys(product_trend[0])
//                   .filter(key => key !== 'period')
//                   .map((product, index) => (
//                     <Line 
//                       key={product}
//                       type="monotone" 
//                       dataKey={product} 
//                       stroke={COLORS[index % COLORS.length]} 
//                       name={product}
//                     />
//                   ))
//                 }
//               </LineChart>
//             </ResponsiveContainer>
//           </CardContent>
//         </Card>

//         {/* Product by Status Breakdown */}
//         <Card>
//           <CardHeader>
//             <CardTitle>Product Quotes by Status</CardTitle>
//           </CardHeader>
//           <CardContent>
//             <ResponsiveContainer width="100%" height={300}>
//               <BarChart data={status_breakdown}>
//                 <CartesianGrid strokeDasharray="3 3" />
//                 <XAxis 
//                   dataKey="product_type"
//                   angle={-45}
//                   textAnchor="end"
//                   height={100}
//                   interval={0}
//                   tick={{ fontSize: 12 }}
//                 />
//                 <YAxis />
//                 <Tooltip />
//                 <Legend />
//                 <Bar dataKey="Budgetary" stackId="a" fill="#fbbf24" name="Budgetary" />
//                 <Bar dataKey="Active" stackId="a" fill="#3b82f6" name="Active" />
//                 <Bar dataKey="Won" stackId="a" fill="#10b981" name="Won" />
//                 <Bar dataKey="Lost" stackId="a" fill="#ef4444" name="Lost" />
//               </BarChart>
//             </ResponsiveContainer>
//           </CardContent>
//         </Card>
//       </div>

//       {/* Data Table */}
//       <Card>
//         <CardHeader>
//           <CardTitle>Detailed Product Performance</CardTitle>
//         </CardHeader>
//         <CardContent>
//           <div className="overflow-x-auto">
//             <table className="w-full text-sm">
//               <thead>
//                 <tr className="border-b">
//                   <th className="text-left p-2">Product Type</th>
//                   <th className="text-right p-2">Quote Count</th>
//                   <th className="text-right p-2">Revenue</th>
//                   <th className="text-right p-2">Avg Value</th>
//                   <th className="text-right p-2">% of Total</th>
//                 </tr>
//               </thead>
//               <tbody>
//                 {revenue_contribution.map((product, index) => (
//                   <tr key={index} className="border-b hover:bg-gray-50">
//                     <td className="p-2 font-medium">{product.product_type}</td>
//                     <td className="text-right p-2">{product.quote_count}</td>
//                     <td className="text-right p-2">${product.revenue.toLocaleString()}</td>
//                     <td className="text-right p-2">${product.avg_value.toLocaleString()}</td>
//                     <td className="text-right p-2">{product.percentage.toFixed(2)}%</td>
//                   </tr>
//                 ))}
//               </tbody>
//             </table>
//           </div>
//         </CardContent>
//       </Card>
//     </div>
//   );
// };

// export default ProductAnalytics;