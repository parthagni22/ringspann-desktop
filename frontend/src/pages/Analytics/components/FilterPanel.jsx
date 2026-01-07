import React, { useState, useEffect } from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { 
  Select, 
  SelectContent, 
  SelectItem, 
  SelectTrigger, 
  SelectValue 
} from '@/components/ui/select';

const eel = window.eel;

const FilterPanel = ({ filters, onFilterChange }) => {
  const [localFilters, setLocalFilters] = useState(filters);
  const [customers, setCustomers] = useState([]);
  const [showCustomDateRange, setShowCustomDateRange] = useState(false);

  useEffect(() => {
    fetchCustomers();
  }, []);

  const fetchCustomers = async () => {
    try {
      // Use Eel to fetch customers from backend
      const result = await eel.get_customers_for_analytics()();
      if (result && result.success) {
        const uniqueCustomers = [...new Set(result.data.map(p => p.customer_name))];
        setCustomers(uniqueCustomers);
      }
    } catch (error) {
      console.error('Error fetching customers:', error);
      // Fallback: empty array
      setCustomers([]);
    }
  };

  const productTypes = [
    { value: 'all', label: 'All Products' },
    { value: '1', label: 'Brake Quotation' },
    { value: '2', label: 'Backstop Quotation' },
    { value: '3', label: 'Couple and Torque Limiter' },
    { value: '4', label: 'Locking Element for Conveyor' },
    { value: '5', label: 'Over Running Clutch' }
  ];

  const quoteStatuses = [
    { value: 'all', label: 'All Statuses' },
    { value: 'Budgetary', label: 'Budgetary' },
    { value: 'Active', label: 'Active' },
    { value: 'Lost', label: 'Lost' },
    { value: 'Won', label: 'Won' }
  ];

  const handleFilterUpdate = (key, value) => {
    const updated = { ...localFilters, [key]: value };
    setLocalFilters(updated);
  };

  const handleApplyFilters = () => {
    onFilterChange(localFilters);
  };

  const handleResetFilters = () => {
    const defaultFilters = {
      dateFilter: 'all',
      startDate: null,
      endDate: null,
      quoteStatus: 'all',
      productType: 'all',
      customer: 'all'
    };
    setLocalFilters(defaultFilters);
    onFilterChange(defaultFilters);
    setShowCustomDateRange(false);
  };

  const handleDateFilterChange = (value) => {
    handleFilterUpdate('dateFilter', value);
    setShowCustomDateRange(value === 'custom');
  };

  return (
    <CardContent className="pt-6">
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4">
        {/* Time Period Filter */}
        <div className="space-y-2">
          <label className="text-sm font-medium text-gray-700">Time Period</label>
          <Select 
            value={localFilters.dateFilter} 
            onValueChange={handleDateFilterChange}
          >
            <SelectTrigger>
              <SelectValue placeholder="Select period" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">All Time</SelectItem>
              <SelectItem value="mtd">Month to Date</SelectItem>
              <SelectItem value="ytd">Year to Date</SelectItem>
              <SelectItem value="custom">Custom Range</SelectItem>
            </SelectContent>
          </Select>
        </div>

        {/* Quote Status Filter */}
        <div className="space-y-2">
          <label className="text-sm font-medium text-gray-700">Quote Status</label>
          <Select 
            value={localFilters.quoteStatus} 
            onValueChange={(value) => handleFilterUpdate('quoteStatus', value)}
          >
            <SelectTrigger>
              <SelectValue placeholder="Select status" />
            </SelectTrigger>
            <SelectContent>
              {quoteStatuses.map(status => (
                <SelectItem key={status.value} value={status.value}>
                  {status.label}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>

        {/* Product Type Filter */}
        <div className="space-y-2">
          <label className="text-sm font-medium text-gray-700">Product Type</label>
          <Select 
            value={localFilters.productType} 
            onValueChange={(value) => handleFilterUpdate('productType', value)}
          >
            <SelectTrigger>
              <SelectValue placeholder="Select product" />
            </SelectTrigger>
            <SelectContent>
              {productTypes.map(product => (
                <SelectItem key={product.value} value={product.value}>
                  {product.label}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>

        {/* Customer Filter */}
        <div className="space-y-2">
          <label className="text-sm font-medium text-gray-700">Customer</label>
          <Select 
            value={localFilters.customer} 
            onValueChange={(value) => handleFilterUpdate('customer', value)}
          >
            <SelectTrigger>
              <SelectValue placeholder="Select customer" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">All Customers</SelectItem>
              {customers.map(customer => (
                <SelectItem key={customer} value={customer}>
                  {customer}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>

        {/* Action Buttons */}
        <div className="space-y-2">
          <label className="text-sm font-medium text-gray-700 invisible">Actions</label>
          <div className="flex gap-2">
            <Button 
              onClick={handleApplyFilters} 
              className="flex-1"
            >
              Apply
            </Button>
            <Button 
              onClick={handleResetFilters} 
              variant="outline"
              className="flex-1"
            >
              Reset
            </Button>
          </div>
        </div>
      </div>

      {/* Custom Date Range */}
      {showCustomDateRange && (
        <div className="mt-4 p-4 bg-gray-50 rounded-lg border border-gray-200">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="space-y-2">
              <label className="text-sm font-medium text-gray-700">Start Date</label>
              <input
                type="date"
                value={localFilters.startDate || ''}
                onChange={(e) => handleFilterUpdate('startDate', e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
            <div className="space-y-2">
              <label className="text-sm font-medium text-gray-700">End Date</label>
              <input
                type="date"
                value={localFilters.endDate || ''}
                onChange={(e) => handleFilterUpdate('endDate', e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
          </div>
        </div>
      )}

      {/* Active Filters Display */}
      <div className="mt-4 flex flex-wrap gap-2">
        {localFilters.dateFilter !== 'all' && (
          <span className="px-3 py-1 bg-blue-100 text-blue-800 text-sm rounded-full">
            Period: {localFilters.dateFilter.toUpperCase()}
          </span>
        )}
        {localFilters.quoteStatus !== 'all' && (
          <span className="px-3 py-1 bg-green-100 text-green-800 text-sm rounded-full">
            Status: {localFilters.quoteStatus}
          </span>
        )}
        {localFilters.productType !== 'all' && (
          <span className="px-3 py-1 bg-purple-100 text-purple-800 text-sm rounded-full">
            Product: {productTypes.find(p => p.value === localFilters.productType)?.label}
          </span>
        )}
        {localFilters.customer !== 'all' && (
          <span className="px-3 py-1 bg-orange-100 text-orange-800 text-sm rounded-full">
            Customer: {localFilters.customer}
          </span>
        )}
      </div>
    </CardContent>
  );
};

export default FilterPanel;