import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import KPICard from './components/KPICard';
import { useCustomerAnalytics, exportAnalyticsData } from './hooks/useAnalyticsData.js';
import {
  BarChart, Bar, PieChart, Pie, Cell,
  XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer
} from 'recharts';
import { Download, Users, DollarSign, TrendingUp, UserCheck, UserPlus } from 'lucide-react';
import { Loader2 } from 'lucide-react';

const COLORS = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6'];

const CustomerAnalytics = ({ filters }) => {
  const { data, loading, error } = useCustomerAnalytics(filters);

  const handleExport = async (format) => {
    const result = await exportAnalyticsData('customer', format, filters);
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
        <span className="ml-2 text-gray-600">Loading customer analytics...</span>
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
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Top Customers by Quote Count */}
        <Card>
          <CardHeader>
            <CardTitle>Top Customers by Quote Count</CardTitle>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={top_customers_by_count.slice(0, 10)}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis 
                  dataKey="customer_name" 
                  angle={-45}
                  textAnchor="end"
                  height={100}
                  interval={0}
                  tick={{ fontSize: 11 }}
                />
                <YAxis />
                <Tooltip />
                <Legend />
                <Bar dataKey="quote_count" fill="#3b82f6" name="Quotes" />
              </BarChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        {/* Top Customers by Revenue */}
        <Card>
          <CardHeader>
            <CardTitle>Top Customers by Revenue</CardTitle>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={top_customers_by_revenue.slice(0, 10)}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis 
                  dataKey="customer_name" 
                  angle={-45}
                  textAnchor="end"
                  height={100}
                  interval={0}
                  tick={{ fontSize: 11 }}
                />
                <YAxis />
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
        {/* Customer Status Breakdown */}
        <Card>
          <CardHeader>
            <CardTitle>Customer Quote Status Breakdown</CardTitle>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={customer_status_breakdown.slice(0, 10)}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis 
                  dataKey="customer_name"
                  angle={-45}
                  textAnchor="end"
                  height={100}
                  interval={0}
                  tick={{ fontSize: 11 }}
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

        {/* New vs Repeat Customers */}
        <Card>
          <CardHeader>
            <CardTitle>New vs Repeat Customers</CardTitle>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={newVsRepeatData}
                  dataKey="value"
                  nameKey="name"
                  cx="50%"
                  cy="50%"
                  outerRadius={100}
                  label={(entry) => `${entry.name}: ${entry.value}`}
                >
                  {newVsRepeatData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip />
                <Legend />
              </PieChart>
            </ResponsiveContainer>
            <div className="mt-4 text-center">
              <p className="text-sm text-gray-600">
                Total: {new_vs_repeat.total} customers
              </p>
              <p className="text-sm text-gray-600">
                Repeat Rate: {((new_vs_repeat.repeat / new_vs_repeat.total) * 100).toFixed(1)}%
              </p>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Data Tables */}
      <div className="grid grid-cols-1 gap-6">
        {/* Top Customers Detail Table */}
        <Card>
          <CardHeader>
            <CardTitle>Top Customer Performance</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead>
                  <tr className="border-b">
                    <th className="text-left p-2">Customer Name</th>
                    <th className="text-right p-2">Quotes</th>
                    <th className="text-right p-2">Total Revenue</th>
                    <th className="text-right p-2">Avg Deal Size</th>
                    <th className="text-right p-2">Last Quote</th>
                  </tr>
                </thead>
                <tbody>
                  {top_customers_by_revenue.slice(0, 10).map((customer, index) => (
                    <tr key={index} className="border-b hover:bg-gray-50">
                      <td className="p-2 font-medium">{customer.customer_name}</td>
                      <td className="text-right p-2">{customer.quote_count}</td>
                      <td className="text-right p-2">${customer.revenue.toLocaleString()}</td>
                      <td className="text-right p-2">${customer.avg_deal_size.toLocaleString()}</td>
                      <td className="text-right p-2">{customer.last_quote_date || 'N/A'}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </CardContent>
        </Card>

        {/* Recent Customer Activity */}
        <Card>
          <CardHeader>
            <CardTitle>Recent Customer Activity</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="overflow-x-auto max-h-96 overflow-y-auto">
              <table className="w-full text-sm">
                <thead className="sticky top-0 bg-white">
                  <tr className="border-b">
                    <th className="text-left p-2">Date</th>
                    <th className="text-left p-2">Customer</th>
                    <th className="text-left p-2">Quotation #</th>
                    <th className="text-left p-2">Status</th>
                  </tr>
                </thead>
                <tbody>
                  {activity_timeline.slice(0, 20).map((activity, index) => (
                    <tr key={index} className="border-b hover:bg-gray-50">
                      <td className="p-2">{activity.date}</td>
                      <td className="p-2 font-medium">{activity.customer_name}</td>
                      <td className="p-2">{activity.quotation_number}</td>
                      <td className="p-2">
                        <span className={`px-2 py-1 rounded-full text-xs ${
                          activity.status === 'Won' ? 'bg-green-100 text-green-800' :
                          activity.status === 'Lost' ? 'bg-red-100 text-red-800' :
                          activity.status === 'Active' ? 'bg-blue-100 text-blue-800' :
                          'bg-yellow-100 text-yellow-800'
                        }`}>
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

export default CustomerAnalytics;