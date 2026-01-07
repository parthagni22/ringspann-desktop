import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { useCombinedInsights, exportAnalyticsData } from './hooks/useAnalyticsData.js';
import {
  BarChart, Bar, LineChart, Line, AreaChart, Area,
  XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, Cell
} from 'recharts';
import { Download, TrendingUp, Filter } from 'lucide-react';
import { Loader2 } from 'lucide-react';

const COLORS = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6'];

const CombinedInsights = ({ filters }) => {
  const { data, loading, error } = useCombinedInsights(filters);

  const handleExport = async (format) => {
    const result = await exportAnalyticsData('combined', format, filters);
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
        <span className="ml-2 text-gray-600">Loading combined insights...</span>
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

  const { 
    product_customer_matrix, 
    top_combinations, 
    funnel, 
    velocity, 
    avg_processing_time,
    product_mix_trend 
  } = data;

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

      {/* Key Metrics Card */}
      <Card>
        <CardHeader>
          <CardTitle>Key Insights</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="p-4 bg-blue-50 rounded-lg">
              <p className="text-sm text-gray-600 mb-1">Avg Processing Time</p>
              <p className="text-2xl font-bold text-blue-900">
                {avg_processing_time ? `${avg_processing_time.toFixed(1)} hrs` : 'N/A'}
              </p>
            </div>
            <div className="p-4 bg-green-50 rounded-lg">
              <p className="text-sm text-gray-600 mb-1">Total Product-Customer Combos</p>
              <p className="text-2xl font-bold text-green-900">
                {top_combinations.length}
              </p>
            </div>
            <div className="p-4 bg-purple-50 rounded-lg">
              <p className="text-sm text-gray-600 mb-1">Active Products</p>
              <p className="text-2xl font-bold text-purple-900">
                {product_customer_matrix.products?.length || 0}
              </p>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Charts Row 1 */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Quote Status Funnel */}
        <Card>
          <CardHeader>
            <CardTitle>Quote Status Funnel</CardTitle>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={funnel} layout="horizontal">
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis type="number" />
                <YAxis dataKey="stage" type="category" width={100} />
                <Tooltip />
                <Legend />
                <Bar dataKey="count" fill="#3b82f6" name="Quote Count" />
              </BarChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        {/* Monthly Quote Velocity */}
        <Card>
          <CardHeader>
            <CardTitle>Monthly Quote Velocity</CardTitle>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={velocity}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="date" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Line 
                  type="monotone" 
                  dataKey="value" 
                  stroke="#10b981" 
                  strokeWidth={2}
                  name="Quotes Created"
                  dot={{ r: 4 }}
                />
              </LineChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>
      </div>

      {/* Product Mix Trend */}
      <Card>
        <CardHeader>
          <CardTitle>Product Mix Trend Over Time</CardTitle>
        </CardHeader>
        <CardContent>
          <ResponsiveContainer width="100%" height={400}>
            <AreaChart data={product_mix_trend}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="period" />
              <YAxis />
              <Tooltip />
              <Legend />
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
      <Card>
        <CardHeader>
          <CardTitle>Top Product-Customer Combinations</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b">
                  <th className="text-left p-2">Customer</th>
                  <th className="text-left p-2">Product</th>
                  <th className="text-right p-2">Quote Count</th>
                  <th className="text-right p-2">Revenue</th>
                </tr>
              </thead>
              <tbody>
                {top_combinations.slice(0, 15).map((combo, index) => (
                  <tr key={index} className="border-b hover:bg-gray-50">
                    <td className="p-2 font-medium">{combo.customer}</td>
                    <td className="p-2">{combo.product}</td>
                    <td className="text-right p-2">{combo.quote_count}</td>
                    <td className="text-right p-2">${combo.revenue.toLocaleString()}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </CardContent>
      </Card>

      {/* Product × Customer Matrix Heatmap */}
      <Card>
        <CardHeader>
          <CardTitle>Product × Customer Matrix</CardTitle>
          <p className="text-sm text-gray-600 mt-1">
            Shows quote count by product and customer combination
          </p>
        </CardHeader>
        <CardContent>
          {product_customer_matrix.customers && product_customer_matrix.products && (
            <div className="overflow-x-auto">
              <table className="w-full text-sm border-collapse">
                <thead>
                  <tr>
                    <th className="border p-2 bg-gray-100 sticky left-0 z-10">Customer</th>
                    {product_customer_matrix.products.map((product, index) => (
                      <th key={index} className="border p-2 bg-gray-100 text-xs">
                        {product}
                      </th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {product_customer_matrix.customers.slice(0, 10).map((customer, idx) => (
                    <tr key={idx}>
                      <td className="border p-2 font-medium bg-gray-50 sticky left-0 z-10 text-xs">
                        {customer}
                      </td>
                      {product_customer_matrix.products.map((product, pidx) => {
                        const value = product_customer_matrix.data[customer]?.[product] || 0;
                        const intensity = value > 0 ? Math.min(value * 20, 100) : 0;
                        
                        return (
                          <td
                            key={pidx}
                            className="border p-2 text-center text-xs"
                            style={{
                              backgroundColor: value > 0 
                                ? `rgba(59, 130, 246, ${intensity / 100})`
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
      <Card>
        <CardHeader>
          <CardTitle>Funnel Conversion Details</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {funnel.map((stage, index) => {
              const nextStage = funnel[index + 1];
              const conversionRate = nextStage 
                ? ((nextStage.count / stage.count) * 100).toFixed(1)
                : null;

              return (
                <div key={index} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                  <div className="flex-1">
                    <h4 className="font-medium text-gray-900">{stage.stage}</h4>
                    <p className="text-sm text-gray-600">
                      {stage.count} quotes • ${stage.value.toLocaleString()} value
                    </p>
                  </div>
                  {conversionRate && (
                    <div className="ml-4 text-right">
                      <p className="text-sm font-medium text-gray-900">
                        {conversionRate}%
                      </p>
                      <p className="text-xs text-gray-600">
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

export default CombinedInsights;