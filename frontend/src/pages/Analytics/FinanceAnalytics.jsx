import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import KPICard from './components/KPICard';
import { useFinanceAnalytics, exportAnalyticsData } from './hooks/useAnalyticsData.js';
import {
  BarChart, Bar, LineChart, Line,
  XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer
} from 'recharts';
import { Download, DollarSign, FileText, TrendingUp, Package } from 'lucide-react';
import { Loader2 } from 'lucide-react';

const FinanceAnalytics = ({ filters }) => {
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
      <div className="flex items-center justify-center h-96">
        <Loader2 className="w-8 h-8 animate-spin text-blue-600" />
        <span className="ml-2 text-gray-600">Loading finance analytics...</span>
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

  const { kpis, revenue_by_status, monthly_trend, product_revenue, value_distribution } = data;

  return (
    <div className="space-y-6">
      {/* Export Buttons */}
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
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Revenue by Status */}
        <Card>
          <CardHeader>
            <CardTitle>Revenue by Quote Status</CardTitle>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={revenue_by_status}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="label" />
                <YAxis />
                <Tooltip formatter={(value) => `$${value.toLocaleString()}`} />
                <Legend />
                <Bar dataKey="value" fill="#3b82f6" name="Revenue" />
              </BarChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        {/* Product Revenue Breakdown */}
        <Card>
          <CardHeader>
            <CardTitle>Revenue by Product Type</CardTitle>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={product_revenue} layout="vertical">
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis type="number" />
                <YAxis 
                  dataKey="product_type" 
                  type="category" 
                  width={150}
                  tick={{ fontSize: 12 }}
                />
                <Tooltip formatter={(value) => `$${value.toLocaleString()}`} />
                <Legend />
                <Bar dataKey="revenue" fill="#10b981" name="Revenue" />
              </BarChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>
      </div>

      {/* Charts Row 2 */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Monthly Revenue Trend */}
        <Card>
          <CardHeader>
            <CardTitle>Monthly Revenue Trend</CardTitle>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={monthly_trend}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="date" />
                <YAxis />
                <Tooltip formatter={(value) => `$${value.toLocaleString()}`} />
                <Legend />
                <Line 
                  type="monotone" 
                  dataKey="value" 
                  stroke="#3b82f6" 
                  strokeWidth={2}
                  name="Revenue"
                  dot={{ r: 4 }}
                />
              </LineChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        {/* Quote Value Distribution */}
        <Card>
          <CardHeader>
            <CardTitle>Quote Value Distribution</CardTitle>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={value_distribution}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis 
                  dataKey="range" 
                  angle={-45}
                  textAnchor="end"
                  height={100}
                  interval={0}
                  tick={{ fontSize: 10 }}
                />
                <YAxis />
                <Tooltip />
                <Legend />
                <Bar dataKey="count" fill="#8b5cf6" name="Quote Count" />
              </BarChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>
      </div>

      {/* Data Tables */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Revenue by Status Table */}
        <Card>
          <CardHeader>
            <CardTitle>Status Breakdown</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead>
                  <tr className="border-b">
                    <th className="text-left p-2">Status</th>
                    <th className="text-right p-2">Quotes</th>
                    <th className="text-right p-2">Revenue</th>
                    <th className="text-right p-2">Avg Value</th>
                  </tr>
                </thead>
                <tbody>
                  {revenue_by_status.map((item, index) => (
                    <tr key={index} className="border-b hover:bg-gray-50">
                      <td className="p-2 font-medium">{item.label}</td>
                      <td className="text-right p-2">{item.metadata.quote_count}</td>
                      <td className="text-right p-2">${item.value.toLocaleString()}</td>
                      <td className="text-right p-2">
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
        <Card>
          <CardHeader>
            <CardTitle>Product Performance</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead>
                  <tr className="border-b">
                    <th className="text-left p-2">Product</th>
                    <th className="text-right p-2">Quotes</th>
                    <th className="text-right p-2">Revenue</th>
                    <th className="text-right p-2">%</th>
                  </tr>
                </thead>
                <tbody>
                  {product_revenue.slice(0, 5).map((product, index) => (
                    <tr key={index} className="border-b hover:bg-gray-50">
                      <td className="p-2 font-medium">{product.product_type}</td>
                      <td className="text-right p-2">{product.quote_count}</td>
                      <td className="text-right p-2">${product.revenue.toLocaleString()}</td>
                      <td className="text-right p-2">{product.percentage.toFixed(1)}%</td>
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

export default FinanceAnalytics;