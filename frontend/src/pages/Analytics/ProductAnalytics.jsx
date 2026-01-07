import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import KPICard from './components/KPICard';
import { useProductAnalytics, exportAnalyticsData } from './hooks/useAnalyticsData.js';
import { 
  BarChart, Bar, LineChart, Line, PieChart, Pie, Cell,
  XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer 
} from 'recharts';
import { Download, Package, TrendingUp, DollarSign, Hash } from 'lucide-react';
import { Loader2 } from 'lucide-react';

const COLORS = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6'];

const ProductAnalytics = ({ filters }) => {
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
      <div className="flex items-center justify-center h-96">
        <Loader2 className="w-8 h-8 animate-spin text-blue-600" />
        <span className="ml-2 text-gray-600">Loading analytics...</span>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex items-center justify-center h-96">
        <div className="text-center">
          <p className="text-red-600 font-medium">{error}</p>
          <Button onClick={() => window.location.reload()} className="mt-4">
            Retry
          </Button>
        </div>
      </div>
    );
  }

  if (!data) return null;

  const { kpis, quote_distribution, revenue_contribution, product_trend, status_breakdown } = data;

  return (
    <div className="space-y-6">
      {/* Export Button */}
      <div className="flex justify-end gap-2">
        <Button 
          variant="outline" 
          onClick={() => handleExport('json')}
          className="flex items-center gap-2"
        >
          <Download className="w-4 h-4" />
          Export JSON
        </Button>
        <Button 
          variant="outline" 
          onClick={() => handleExport('csv')}
          className="flex items-center gap-2"
        >
          <Download className="w-4 h-4" />
          Export CSV
        </Button>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4">
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
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Product Quote Distribution */}
        <Card>
          <CardHeader>
            <CardTitle>Quote Distribution by Product</CardTitle>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={quote_distribution}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis 
                  dataKey="product_type" 
                  angle={-45}
                  textAnchor="end"
                  height={100}
                  interval={0}
                  tick={{ fontSize: 12 }}
                />
                <YAxis />
                <Tooltip />
                <Legend />
                <Bar dataKey="quote_count" fill="#3b82f6" name="Quote Count" />
              </BarChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        {/* Revenue Contribution */}
        <Card>
          <CardHeader>
            <CardTitle>Revenue Contribution by Product</CardTitle>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={revenue_contribution}
                  dataKey="revenue"
                  nameKey="product_type"
                  cx="50%"
                  cy="50%"
                  outerRadius={100}
                  label={(entry) => `${entry.product_type}: ${entry.percentage.toFixed(1)}%`}
                >
                  {revenue_contribution.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip formatter={(value) => `$${value.toLocaleString()}`} />
              </PieChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>
      </div>

      {/* Charts Row 2 */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Product Trend Over Time */}
        <Card>
          <CardHeader>
            <CardTitle>Product Quotes Trend Over Time</CardTitle>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={product_trend}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="period" />
                <YAxis />
                <Tooltip />
                <Legend />
                {product_trend.length > 0 && Object.keys(product_trend[0])
                  .filter(key => key !== 'period')
                  .map((product, index) => (
                    <Line 
                      key={product}
                      type="monotone" 
                      dataKey={product} 
                      stroke={COLORS[index % COLORS.length]} 
                      name={product}
                    />
                  ))
                }
              </LineChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        {/* Product by Status Breakdown */}
        <Card>
          <CardHeader>
            <CardTitle>Product Quotes by Status</CardTitle>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={status_breakdown}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis 
                  dataKey="product_type"
                  angle={-45}
                  textAnchor="end"
                  height={100}
                  interval={0}
                  tick={{ fontSize: 12 }}
                />
                <YAxis />
                <Tooltip />
                <Legend />
                <Bar dataKey="Budgetary" stackId="a" fill="#fbbf24" name="Budgetary" />
                <Bar dataKey="Active" stackId="a" fill="#3b82f6" name="Active" />
                <Bar dataKey="Won" stackId="a" fill="#10b981" name="Won" />
                <Bar dataKey="Lost" stackId="a" fill="#ef4444" name="Lost" />
              </BarChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>
      </div>

      {/* Data Table */}
      <Card>
        <CardHeader>
          <CardTitle>Detailed Product Performance</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b">
                  <th className="text-left p-2">Product Type</th>
                  <th className="text-right p-2">Quote Count</th>
                  <th className="text-right p-2">Revenue</th>
                  <th className="text-right p-2">Avg Value</th>
                  <th className="text-right p-2">% of Total</th>
                </tr>
              </thead>
              <tbody>
                {revenue_contribution.map((product, index) => (
                  <tr key={index} className="border-b hover:bg-gray-50">
                    <td className="p-2 font-medium">{product.product_type}</td>
                    <td className="text-right p-2">{product.quote_count}</td>
                    <td className="text-right p-2">${product.revenue.toLocaleString()}</td>
                    <td className="text-right p-2">${product.avg_value.toLocaleString()}</td>
                    <td className="text-right p-2">{product.percentage.toFixed(2)}%</td>
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

export default ProductAnalytics;