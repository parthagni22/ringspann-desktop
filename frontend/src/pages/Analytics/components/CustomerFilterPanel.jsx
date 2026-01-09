import React, { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Calendar, Filter, RotateCcw } from 'lucide-react';

const CustomerFilterPanel = ({ filters, onFilterChange }) => {
  const [localFilters, setLocalFilters] = useState(filters);

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
      customer: 'all',
      quoteStatus: 'all',
    };
    setLocalFilters(resetFilters);
    onFilterChange(resetFilters);
  };

  return (
    <div style={styles.container}>
      <div style={styles.header}>
        <div style={styles.headerLeft}>
          <Filter style={styles.filterIcon} />
          <span style={styles.headerTitle}>Customer Filters</span>
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
            <option value="week">This Week</option>
            <option value="month">This Month</option>
            <option value="quarter">This Quarter</option>
            <option value="year">This Year</option>
            <option value="custom">Custom Range</option>
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
            {/* Dynamic customer options will be loaded here */}
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

        {/* Action Buttons */}
        <div style={styles.actionButtons}>
          <Button onClick={handleApply} style={styles.applyButton}>
            <Filter className="w-4 h-4" style={{ marginRight: '6px' }} />
            Apply
          </Button>
          <Button onClick={handleReset} variant="outline" style={styles.resetButton}>
            <RotateCcw className="w-4 h-4" style={{ marginRight: '6px' }} />
            Reset
          </Button>
        </div>
      </div>

      {/* Custom Date Range */}
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
    marginBottom: '24px',
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
    color: '#f59e0b',
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
    backgroundColor: '#f59e0b',
    color: '#ffffff',
    border: 'none',
    borderRadius: '6px',
    cursor: 'pointer',
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

export default CustomerFilterPanel;