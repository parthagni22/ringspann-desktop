import React, { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Calendar, Filter, RotateCcw } from 'lucide-react';

const FilterPanel = ({ filters, onFilterChange }) => {
  const [localFilters, setLocalFilters] = useState(filters);

  // Get max date (today)
  const getMaxDate = () => {
    return new Date().toISOString().split('T')[0];
  };

  // Get min date (365 days ago)
  const getMinDate = () => {
    const date = new Date();
    date.setDate(date.getDate() - 365);
    return date.toISOString().split('T')[0];
  };

  const handleChange = (key, value) => {
    setLocalFilters(prev => ({ ...prev, [key]: value }));
  };

  const handleApply = () => {
    onFilterChange(localFilters);
  };

  const handleReset = () => {
    const resetFilters = {
      dateFilter: 'all',
      startDate: null,
      endDate: null,
      quoteStatus: 'all',
      productType: 'all',
      customer: 'all'
    };
    setLocalFilters(resetFilters);
    onFilterChange(resetFilters);
  };

  return (
    <div style={styles.container}>
      <div style={styles.header}>
        <div style={styles.headerLeft}>
          <Filter style={styles.filterIcon} />
          <span style={styles.headerTitle}>Filters</span>
        </div>
      </div>

      <div style={styles.filtersGrid}>
        {/* Time Period Filter */}
        <div style={styles.filterGroup}>
          <label style={styles.label}>Time Period</label>
          <select
            value={localFilters.dateFilter}
            onChange={(e) => handleChange('dateFilter', e.target.value)}
            style={styles.select}
          >
            <option value="all">All Time</option>
            <option value="today">Today</option>
            <option value="custom">Custom Range (Last 365 Days)</option>
          </select>
        </div>

        {/* Quote Status Filter */}
        <div style={styles.filterGroup}>
          <label style={styles.label}>Quote Status</label>
          <select
            value={localFilters.quoteStatus}
            onChange={(e) => handleChange('quoteStatus', e.target.value)}
            style={styles.select}
          >
            <option value="all">All Statuses</option>
            <option value="Budgetary">Budgetary</option>
            <option value="Active">Active</option>
            <option value="Won">Won</option>
            <option value="Lost">Lost</option>
          </select>
        </div>

        {/* Product Type Filter */}
        <div style={styles.filterGroup}>
          <label style={styles.label}>Product Type</label>
          <select
            value={localFilters.productType}
            onChange={(e) => handleChange('productType', e.target.value)}
            style={styles.select}
          >
            <option value="all">All Products</option>
            <option value="Brake Quotation">Brake Quotation</option>
            <option value="Backstop Quotation">Backstop Quotation</option>
            <option value="Couple and Torque Limiter">Couple and Torque Limiter</option>
            <option value="Locking Element for Conveyor">Locking Element for Conveyor</option>
            <option value="Over Running Clutch">Over Running Clutch</option>
          </select>
        </div>

        {/* Customer Filter */}
        <div style={styles.filterGroup}>
          <label style={styles.label}>Customer</label>
          <select
            value={localFilters.customer}
            onChange={(e) => handleChange('customer', e.target.value)}
            style={styles.select}
          >
            <option value="all">All Customers</option>
            {/* Add dynamic customer options here */}
          </select>
        </div>

        {/* Action Buttons */}
        <div style={styles.actionButtons}>
          <Button
            onClick={handleApply}
            style={styles.applyButton}
          >
            <Filter className="w-4 h-4" style={{ marginRight: '6px' }} />
            Apply Filters
          </Button>
          <Button
            onClick={handleReset}
            variant="outline"
            style={styles.resetButton}
          >
            <RotateCcw className="w-4 h-4" style={{ marginRight: '6px' }} />
            Reset
          </Button>
        </div>
      </div>

      {/* Custom Date Range (shown when custom is selected) */}
      {localFilters.dateFilter === 'custom' && (
        <div style={styles.customDateRange}>
          <div style={styles.filterGroup}>
            <label style={styles.label}>Start Date</label>
            <div style={styles.dateInputWrapper}>
              <Calendar className="w-4 h-4" style={styles.calendarIcon} />
              <input
                type="date"
                value={localFilters.startDate || ''}
                onChange={(e) => handleChange('startDate', e.target.value)}
                min={getMinDate()}
                max={getMaxDate()}
                style={styles.dateInput}
              />
            </div>
          </div>
          <div style={styles.filterGroup}>
            <label style={styles.label}>End Date</label>
            <div style={styles.dateInputWrapper}>
              <Calendar className="w-4 h-4" style={styles.calendarIcon} />
              <input
                type="date"
                value={localFilters.endDate || ''}
                onChange={(e) => handleChange('endDate', e.target.value)}
                min={getMinDate()}
                max={getMaxDate()}
                style={styles.dateInput}
              />
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

const styles = {
  container: {
    backgroundColor: '#ffffff',
    borderRadius: '8px',
    padding: '20px',
    border: '1px solid #e5e7eb',
  },
  header: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: '20px',
    paddingBottom: '12px',
    borderBottom: '2px solid #e5e7eb',
  },
  headerLeft: {
    display: 'flex',
    alignItems: 'center',
    gap: '10px',
  },
  filterIcon: {
    width: '20px',
    height: '20px',
    color: '#3b82f6',
  },
  headerTitle: {
    fontSize: '18px',
    fontWeight: '600',
    color: '#111827',
  },
  filtersGrid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
    gap: '16px',
    alignItems: 'end',
  },
  filterGroup: {
    display: 'flex',
    flexDirection: 'column',
    gap: '8px',
  },
  label: {
    fontSize: '14px',
    fontWeight: '500',
    color: '#374151',
    marginBottom: '4px',
  },
  select: {
    width: '100%',
    padding: '10px 12px',
    fontSize: '14px',
    border: '1px solid #d1d5db',
    borderRadius: '6px',
    backgroundColor: '#ffffff',
    color: '#1f2937',
    cursor: 'pointer',
    transition: 'all 0.2s',
    outline: 'none',
  },
  actionButtons: {
    display: 'flex',
    gap: '10px',
    alignItems: 'center',
  },
  applyButton: {
    display: 'flex',
    alignItems: 'center',
    padding: '10px 20px',
    fontSize: '14px',
    fontWeight: '500',
    backgroundColor: '#3b82f6',
    color: '#ffffff',
    border: 'none',
    borderRadius: '6px',
    cursor: 'pointer',
    transition: 'background-color 0.2s',
    whiteSpace: 'nowrap',
  },
  resetButton: {
    display: 'flex',
    alignItems: 'center',
    padding: '10px 20px',
    fontSize: '14px',
    fontWeight: '500',
    backgroundColor: '#ffffff',
    color: '#6b7280',
    border: '1px solid #d1d5db',
    borderRadius: '6px',
    cursor: 'pointer',
    transition: 'all 0.2s',
    whiteSpace: 'nowrap',
  },
  customDateRange: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
    gap: '16px',
    marginTop: '20px',
    paddingTop: '20px',
    borderTop: '1px solid #e5e7eb',
  },
  dateInputWrapper: {
    position: 'relative',
    display: 'flex',
    alignItems: 'center',
  },
  calendarIcon: {
    position: 'absolute',
    left: '12px',
    color: '#6b7280',
    pointerEvents: 'none',
  },
  dateInput: {
    width: '100%',
    padding: '10px 12px 10px 40px',
    fontSize: '14px',
    border: '1px solid #d1d5db',
    borderRadius: '6px',
    backgroundColor: '#ffffff',
    color: '#1f2937',
    outline: 'none',
  },
};

// Add hover effects via CSS
const styleSheet = document.createElement('style');
styleSheet.textContent = `
  select:hover {
    border-color: #3b82f6 !important;
  }
  select:focus {
    border-color: #3b82f6 !important;
    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1) !important;
  }
  input[type="date"]:hover {
    border-color: #3b82f6 !important;
  }
  input[type="date"]:focus {
    border-color: #3b82f6 !important;
    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1) !important;
  }
`;
document.head.appendChild(styleSheet);

export default FilterPanel;














// import React, { useState, useEffect } from 'react';
// import { Card, CardContent } from '@/components/ui/card';
// import { Button } from '@/components/ui/button';
// import { 
//   Select, 
//   SelectContent, 
//   SelectItem, 
//   SelectTrigger, 
//   SelectValue 
// } from '@/components/ui/select';

// const eel = window.eel;

// const FilterPanel = ({ filters, onFilterChange }) => {
//   const [localFilters, setLocalFilters] = useState(filters);
//   const [customers, setCustomers] = useState([]);
//   const [showCustomDateRange, setShowCustomDateRange] = useState(false);

//   useEffect(() => {
//     fetchCustomers();
//   }, []);

//   const fetchCustomers = async () => {
//     try {
//       // Use Eel to fetch customers from backend
//       const result = await eel.get_customers_for_analytics()();
//       if (result && result.success) {
//         const uniqueCustomers = [...new Set(result.data.map(p => p.customer_name))];
//         setCustomers(uniqueCustomers);
//       }
//     } catch (error) {
//       console.error('Error fetching customers:', error);
//       // Fallback: empty array
//       setCustomers([]);
//     }
//   };

//   const productTypes = [
//     { value: 'all', label: 'All Products' },
//     { value: '1', label: 'Brake Quotation' },
//     { value: '2', label: 'Backstop Quotation' },
//     { value: '3', label: 'Couple and Torque Limiter' },
//     { value: '4', label: 'Locking Element for Conveyor' },
//     { value: '5', label: 'Over Running Clutch' }
//   ];

//   const quoteStatuses = [
//     { value: 'all', label: 'All Statuses' },
//     { value: 'Budgetary', label: 'Budgetary' },
//     { value: 'Active', label: 'Active' },
//     { value: 'Lost', label: 'Lost' },
//     { value: 'Won', label: 'Won' }
//   ];

//   const handleFilterUpdate = (key, value) => {
//     const updated = { ...localFilters, [key]: value };
//     setLocalFilters(updated);
//   };

//   const handleApplyFilters = () => {
//     onFilterChange(localFilters);
//   };

//   const handleResetFilters = () => {
//     const defaultFilters = {
//       dateFilter: 'all',
//       startDate: null,
//       endDate: null,
//       quoteStatus: 'all',
//       productType: 'all',
//       customer: 'all'
//     };
//     setLocalFilters(defaultFilters);
//     onFilterChange(defaultFilters);
//     setShowCustomDateRange(false);
//   };

//   const handleDateFilterChange = (value) => {
//     handleFilterUpdate('dateFilter', value);
//     setShowCustomDateRange(value === 'custom');
//   };

//   return (
//     <CardContent className="pt-6">
//       <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4">
//         {/* Time Period Filter */}
//         <div className="space-y-2">
//           <label className="text-sm font-medium text-gray-700">Time Period</label>
//           <Select 
//             value={localFilters.dateFilter} 
//             onValueChange={handleDateFilterChange}
//           >
//             <SelectTrigger>
//               <SelectValue placeholder="Select period" />
//             </SelectTrigger>
//             <SelectContent>
//               <SelectItem value="all">All Time</SelectItem>
//               <SelectItem value="mtd">Month to Date</SelectItem>
//               <SelectItem value="ytd">Year to Date</SelectItem>
//               <SelectItem value="custom">Custom Range</SelectItem>
//             </SelectContent>
//           </Select>
//         </div>

//         {/* Quote Status Filter */}
//         <div className="space-y-2">
//           <label className="text-sm font-medium text-gray-700">Quote Status</label>
//           <Select 
//             value={localFilters.quoteStatus} 
//             onValueChange={(value) => handleFilterUpdate('quoteStatus', value)}
//           >
//             <SelectTrigger>
//               <SelectValue placeholder="Select status" />
//             </SelectTrigger>
//             <SelectContent>
//               {quoteStatuses.map(status => (
//                 <SelectItem key={status.value} value={status.value}>
//                   {status.label}
//                 </SelectItem>
//               ))}
//             </SelectContent>
//           </Select>
//         </div>

//         {/* Product Type Filter */}
//         <div className="space-y-2">
//           <label className="text-sm font-medium text-gray-700">Product Type</label>
//           <Select 
//             value={localFilters.productType} 
//             onValueChange={(value) => handleFilterUpdate('productType', value)}
//           >
//             <SelectTrigger>
//               <SelectValue placeholder="Select product" />
//             </SelectTrigger>
//             <SelectContent>
//               {productTypes.map(product => (
//                 <SelectItem key={product.value} value={product.value}>
//                   {product.label}
//                 </SelectItem>
//               ))}
//             </SelectContent>
//           </Select>
//         </div>

//         {/* Customer Filter */}
//         <div className="space-y-2">
//           <label className="text-sm font-medium text-gray-700">Customer</label>
//           <Select 
//             value={localFilters.customer} 
//             onValueChange={(value) => handleFilterUpdate('customer', value)}
//           >
//             <SelectTrigger>
//               <SelectValue placeholder="Select customer" />
//             </SelectTrigger>
//             <SelectContent>
//               <SelectItem value="all">All Customers</SelectItem>
//               {customers.map(customer => (
//                 <SelectItem key={customer} value={customer}>
//                   {customer}
//                 </SelectItem>
//               ))}
//             </SelectContent>
//           </Select>
//         </div>

//         {/* Action Buttons */}
//         <div className="space-y-2">
//           <label className="text-sm font-medium text-gray-700 invisible">Actions</label>
//           <div className="flex gap-2">
//             <Button 
//               onClick={handleApplyFilters} 
//               className="flex-1"
//             >
//               Apply
//             </Button>
//             <Button 
//               onClick={handleResetFilters} 
//               variant="outline"
//               className="flex-1"
//             >
//               Reset
//             </Button>
//           </div>
//         </div>
//       </div>

//       {/* Custom Date Range */}
//       {showCustomDateRange && (
//         <div className="mt-4 p-4 bg-gray-50 rounded-lg border border-gray-200">
//           <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
//             <div className="space-y-2">
//               <label className="text-sm font-medium text-gray-700">Start Date</label>
//               <input
//                 type="date"
//                 value={localFilters.startDate || ''}
//                 onChange={(e) => handleFilterUpdate('startDate', e.target.value)}
//                 className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
//               />
//             </div>
//             <div className="space-y-2">
//               <label className="text-sm font-medium text-gray-700">End Date</label>
//               <input
//                 type="date"
//                 value={localFilters.endDate || ''}
//                 onChange={(e) => handleFilterUpdate('endDate', e.target.value)}
//                 className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
//               />
//             </div>
//           </div>
//         </div>
//       )}

//       {/* Active Filters Display */}
//       <div className="mt-4 flex flex-wrap gap-2">
//         {localFilters.dateFilter !== 'all' && (
//           <span className="px-3 py-1 bg-blue-100 text-blue-800 text-sm rounded-full">
//             Period: {localFilters.dateFilter.toUpperCase()}
//           </span>
//         )}
//         {localFilters.quoteStatus !== 'all' && (
//           <span className="px-3 py-1 bg-green-100 text-green-800 text-sm rounded-full">
//             Status: {localFilters.quoteStatus}
//           </span>
//         )}
//         {localFilters.productType !== 'all' && (
//           <span className="px-3 py-1 bg-purple-100 text-purple-800 text-sm rounded-full">
//             Product: {productTypes.find(p => p.value === localFilters.productType)?.label}
//           </span>
//         )}
//         {localFilters.customer !== 'all' && (
//           <span className="px-3 py-1 bg-orange-100 text-orange-800 text-sm rounded-full">
//             Customer: {localFilters.customer}
//           </span>
//         )}
//       </div>
//     </CardContent>
//   );
// };

// export default FilterPanel;