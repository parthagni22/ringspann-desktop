import React from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { TrendingUp, TrendingDown, Minus } from 'lucide-react';

const KPICard = ({ 
  label, 
  value, 
  changePercent = null, 
  changeDirection = 'neutral',
  formatType = 'number',
  icon: Icon = null 
}) => {
  const formatValue = (val, type) => {
    if (val === null || val === undefined) return 'N/A';
    
    switch (type) {
      case 'currency':
        return new Intl.NumberFormat('en-US', {
          style: 'currency',
          currency: 'USD',
          minimumFractionDigits: 0,
          maximumFractionDigits: 0
        }).format(val);
      
      case 'percent':
        return `${val.toFixed(2)}%`;
      
      case 'number':
        return new Intl.NumberFormat('en-US').format(val);
      
      case 'text':
      default:
        return val;
    }
  };

  const getTrendIcon = () => {
    switch (changeDirection) {
      case 'up':
        return <TrendingUp className="w-4 h-4 text-green-600" />;
      case 'down':
        return <TrendingDown className="w-4 h-4 text-red-600" />;
      default:
        return <Minus className="w-4 h-4 text-gray-400" />;
    }
  };

  const getTrendColor = () => {
    switch (changeDirection) {
      case 'up':
        return 'text-green-600';
      case 'down':
        return 'text-red-600';
      default:
        return 'text-gray-400';
    }
  };

  return (
    <Card className="hover:shadow-lg transition-shadow duration-200">
      <CardContent className="pt-6">
        <div className="flex items-start justify-between mb-2">
          <div className="flex-1">
            <p className="text-sm font-medium text-gray-600 mb-1">{label}</p>
            <h3 className="text-2xl font-bold text-gray-900">
              {formatValue(value, formatType)}
            </h3>
          </div>
          {Icon && (
            <div className="p-2 bg-blue-50 rounded-lg">
              <Icon className="w-6 h-6 text-blue-600" />
            </div>
          )}
        </div>
        
        {changePercent !== null && (
          <div className="flex items-center gap-1 mt-2">
            {getTrendIcon()}
            <span className={`text-sm font-medium ${getTrendColor()}`}>
              {Math.abs(changePercent)}%
            </span>
            <span className="text-sm text-gray-500 ml-1">
              vs previous period
            </span>
          </div>
        )}
      </CardContent>
    </Card>
  );
};

export default KPICard;