import React from 'react';
import { TrendingUp, TrendingDown, Minus } from 'lucide-react';

const KPICard = ({ 
  label, 
  value, 
  changePercent, 
  changeDirection, 
  formatType = 'number',
  icon: Icon 
}) => {
  
  const formatValue = (val, type) => {
    if (val === null || val === undefined) return 'N/A';
    
    switch (type) {
      case 'currency':
        return `$${val.toLocaleString()}`;
      case 'number':
        return val.toLocaleString();
      case 'percentage':
        return `${val}%`;
      case 'text':
        return val;
      default:
        return val;
    }
  };

  const getTrendIcon = () => {
    if (!changeDirection) return null;
    
    switch (changeDirection) {
      case 'up':
        return <TrendingUp style={styles.trendIconUp} />;
      case 'down':
        return <TrendingDown style={styles.trendIconDown} />;
      default:
        return <Minus style={styles.trendIconNeutral} />;
    }
  };

  const getTrendColor = () => {
    if (!changeDirection) return '#6b7280';
    
    switch (changeDirection) {
      case 'up':
        return '#10b981';
      case 'down':
        return '#ef4444';
      default:
        return '#6b7280';
    }
  };

  return (
    <div style={styles.card}>
      <div style={styles.header}>
        <div style={styles.iconWrapper}>
          {Icon && <Icon style={styles.icon} />}
        </div>
        {changePercent !== null && changePercent !== undefined && (
          <div style={{ ...styles.changeBadge, backgroundColor: `${getTrendColor()}15` }}>
            {getTrendIcon()}
            <span style={{ ...styles.changeText, color: getTrendColor() }}>
              {Math.abs(changePercent)}%
            </span>
          </div>
        )}
      </div>
      
      <div style={styles.content}>
        <div style={styles.label}>{label}</div>
        <div style={styles.value}>{formatValue(value, formatType)}</div>
      </div>
    </div>
  );
};

const styles = {
  card: {
    backgroundColor: '#ffffff',
    borderRadius: '12px',
    padding: '20px',
    border: '1px solid #e5e7eb',
    boxShadow: '0 1px 3px rgba(0, 0, 0, 0.06)',
    transition: 'all 0.3s ease',
    cursor: 'default',
    height: '100%',
    display: 'flex',
    flexDirection: 'column',
    justifyContent: 'space-between',
  },
  header: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
    marginBottom: '16px',
  },
  iconWrapper: {
    width: '48px',
    height: '48px',
    borderRadius: '10px',
    backgroundColor: '#eff6ff',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
  },
  icon: {
    width: '24px',
    height: '24px',
    color: '#3b82f6',
  },
  changeBadge: {
    display: 'flex',
    alignItems: 'center',
    gap: '4px',
    padding: '4px 10px',
    borderRadius: '20px',
  },
  trendIconUp: {
    width: '16px',
    height: '16px',
    color: '#10b981',
  },
  trendIconDown: {
    width: '16px',
    height: '16px',
    color: '#ef4444',
  },
  trendIconNeutral: {
    width: '16px',
    height: '16px',
    color: '#6b7280',
  },
  changeText: {
    fontSize: '13px',
    fontWeight: '600',
  },
  content: {
    display: 'flex',
    flexDirection: 'column',
    gap: '8px',
  },
  label: {
    fontSize: '14px',
    fontWeight: '500',
    color: '#6b7280',
    lineHeight: '1.4',
  },
  value: {
    fontSize: '28px',
    fontWeight: '700',
    color: '#111827',
    lineHeight: '1.2',
  },
};

// Add hover effect via CSS
const styleSheet = document.createElement('style');
styleSheet.textContent = `
  div[style*="backgroundColor: #ffffff"][style*="borderRadius: 12px"]:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1) !important;
  }
`;
if (!document.querySelector('style[data-kpi-card-styles]')) {
  styleSheet.setAttribute('data-kpi-card-styles', '');
  document.head.appendChild(styleSheet);
}

export default KPICard;















// import React from 'react';
// import { Card, CardContent } from '@/components/ui/card';
// import { TrendingUp, TrendingDown, Minus } from 'lucide-react';

// const KPICard = ({ 
//   label, 
//   value, 
//   changePercent = null, 
//   changeDirection = 'neutral',
//   formatType = 'number',
//   icon: Icon = null 
// }) => {
//   const formatValue = (val, type) => {
//     if (val === null || val === undefined) return 'N/A';
    
//     switch (type) {
//       case 'currency':
//         return new Intl.NumberFormat('en-US', {
//           style: 'currency',
//           currency: 'USD',
//           minimumFractionDigits: 0,
//           maximumFractionDigits: 0
//         }).format(val);
      
//       case 'percent':
//         return `${val.toFixed(2)}%`;
      
//       case 'number':
//         return new Intl.NumberFormat('en-US').format(val);
      
//       case 'text':
//       default:
//         return val;
//     }
//   };

//   const getTrendIcon = () => {
//     switch (changeDirection) {
//       case 'up':
//         return <TrendingUp className="w-4 h-4 text-green-600" />;
//       case 'down':
//         return <TrendingDown className="w-4 h-4 text-red-600" />;
//       default:
//         return <Minus className="w-4 h-4 text-gray-400" />;
//     }
//   };

//   const getTrendColor = () => {
//     switch (changeDirection) {
//       case 'up':
//         return 'text-green-600';
//       case 'down':
//         return 'text-red-600';
//       default:
//         return 'text-gray-400';
//     }
//   };

//   return (
//     <Card className="hover:shadow-lg transition-shadow duration-200">
//       <CardContent className="pt-6">
//         <div className="flex items-start justify-between mb-2">
//           <div className="flex-1">
//             <p className="text-sm font-medium text-gray-600 mb-1">{label}</p>
//             <h3 className="text-2xl font-bold text-gray-900">
//               {formatValue(value, formatType)}
//             </h3>
//           </div>
//           {Icon && (
//             <div className="p-2 bg-blue-50 rounded-lg">
//               <Icon className="w-6 h-6 text-blue-600" />
//             </div>
//           )}
//         </div>
        
//         {changePercent !== null && (
//           <div className="flex items-center gap-1 mt-2">
//             {getTrendIcon()}
//             <span className={`text-sm font-medium ${getTrendColor()}`}>
//               {Math.abs(changePercent)}%
//             </span>
//             <span className="text-sm text-gray-500 ml-1">
//               vs previous period
//             </span>
//           </div>
//         )}
//       </CardContent>
//     </Card>
//   );
// };

// export default KPICard;