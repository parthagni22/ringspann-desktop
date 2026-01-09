import { useState, useEffect } from 'react';

const eel = window.eel;

export const useAnalyticsData = (eelFunction, filters, dependencies = []) => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchData();
  }, [...dependencies, JSON.stringify(filters)]);

  const fetchData = async () => {
    setLoading(true);
    setError(null);

    try {
      const result = await eelFunction(
        filters.dateFilter || 'all',
        filters.startDate || null,
        filters.endDate || null,
        filters.quoteStatus || 'all',
        filters.customer || 'all',
        filters.productType || 'all'
      )();

      if (result && result.success) {
        setData(result.data);
      } else {
        setError(result?.error || 'Failed to fetch data');
      }
    } catch (err) {
      console.error('Error:', err);
      setError('Failed to fetch data');
    } finally {
      setLoading(false);
    }
  };

  return { data, loading, error, refetch: fetchData };
};

export const useProductAnalytics = (filters) => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchData();
  }, [JSON.stringify(filters)]);

  const fetchData = async () => {
    setLoading(true);
    setError(null);

    try {
      const result = await eel.get_product_analytics(
        filters.dateFilter || 'all',
        filters.startDate || null,
        filters.endDate || null,
        filters.quoteStatus || 'all',
        filters.customer || 'all',
        filters.productType || 'all'  // ADD THIS
      )();

      if (result && result.success) {
        setData(result.data);
      } else {
        setError(result?.error || 'Failed to fetch data');
      }
    } catch (err) {
      console.error('Error:', err);
      setError('Failed to fetch data');
    } finally {
      setLoading(false);
    }
  };

  return { data, loading, error, refetch: fetchData };
};

export const useFinanceAnalytics = (filters) => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchData();
  }, [JSON.stringify(filters)]);

  const fetchData = async () => {
    setLoading(true);
    setError(null);

    try {
      const result = await eel.get_finance_analytics(
        filters.dateFilter || 'all',
        filters.startDate || null,
        filters.endDate || null,
        filters.quoteStatus || 'all',
        filters.productType || 'all',
        filters.customer || 'all'
      )();

      if (result && result.success) {
        setData(result.data);
      } else {
        setError(result?.error || 'Failed to fetch data');
      }
    } catch (err) {
      console.error('Error:', err);
      setError('Failed to fetch data');
    } finally {
      setLoading(false);
    }
  };

  return { data, loading, error, refetch: fetchData };
};

export const useCustomerAnalytics = (filters) => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchData();
  }, [JSON.stringify(filters)]);

  const fetchData = async () => {
    setLoading(true);
    setError(null);

    try {
      const result = await eel.get_customer_analytics(
        filters.dateFilter || 'all',
        filters.startDate || null,
        filters.endDate || null,
        filters.quoteStatus || 'all',
        filters.productType || 'all'
      )();

      if (result && result.success) {
        setData(result.data);
      } else {
        setError(result?.error || 'Failed to fetch data');
      }
    } catch (err) {
      console.error('Error:', err);
      setError('Failed to fetch data');
    } finally {
      setLoading(false);
    }
  };

  return { data, loading, error, refetch: fetchData };
};

export const useCombinedInsights = (filters) => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchData();
  }, [JSON.stringify(filters)]);

  const fetchData = async () => {
    setLoading(true);
    setError(null);

    try {
      // Combined insights only needs 3 params
      const result = await eel.get_combined_insights(
        filters.dateFilter || 'all',
        filters.startDate || null,
        filters.endDate || null
      )();

      if (result && result.success) {
        setData(result.data);
      } else {
        setError(result?.error || 'Failed to fetch data');
      }
    } catch (err) {
      console.error('Error:', err);
      setError('Failed to fetch data');
    } finally {
      setLoading(false);
    }
  };

  return { data, loading, error, refetch: fetchData };
};

export const exportAnalyticsData = async (view, format, filters) => {
  try {
    const result = await eel.export_analytics_data(
      view,
      format,
      filters.dateFilter || 'all',
      filters.startDate || null,
      filters.endDate || null
    )();

    return result;
  } catch (error) {
    console.error('Export error:', error);
    return { success: false, error: error.message };
  }
};



























// import { useState, useEffect } from 'react';

// const eel = window.eel;

// export const useAnalyticsData = (eelFunction, filters, dependencies = []) => {
//   const [data, setData] = useState(null);
//   const [loading, setLoading] = useState(true);
//   const [error, setError] = useState(null);

//   useEffect(() => {
//     fetchData();
//   }, [...dependencies, JSON.stringify(filters)]);

//   const fetchData = async () => {
//     setLoading(true);
//     setError(null);

//     try {
//       const result = await eelFunction(
//         filters.dateFilter || 'all',
//         filters.startDate || null,
//         filters.endDate || null,
//         filters.quoteStatus || 'all',
//         filters.customer || 'all'
//       )();

//       if (result.success) {
//         setData(result.data);
//       } else {
//         setError(result.error || 'Failed to fetch data');
//       }
//     } catch (err) {
//       console.error('Error:', err);
//       setError('Failed to fetch data');
//     } finally {
//       setLoading(false);
//     }
//   };

//   return { data, loading, error, refetch: fetchData };
// };

// export const useProductAnalytics = (filters) => {
//   return useAnalyticsData(eel.get_product_analytics, filters);
// };

// export const useFinanceAnalytics = (filters) => {
//   const [data, setData] = useState(null);
//   const [loading, setLoading] = useState(true);
//   const [error, setError] = useState(null);

//   useEffect(() => {
//     fetchData();
//   }, [JSON.stringify(filters)]);

//   const fetchData = async () => {
//     setLoading(true);
//     setError(null);

//     try {
//       const result = await eel.get_finance_analytics(
//         filters.dateFilter || 'all',
//         filters.startDate || null,
//         filters.endDate || null,
//         filters.quoteStatus || 'all',
//         filters.productType || 'all',
//         filters.customer || 'all'
//       )();

//       if (result.success) {
//         setData(result.data);
//       } else {
//         setError(result.error || 'Failed to fetch data');
//       }
//     } catch (err) {
//       console.error('Error:', err);
//       setError('Failed to fetch data');
//     } finally {
//       setLoading(false);
//     }
//   };

//   return { data, loading, error, refetch: fetchData };
// };

// export const useCustomerAnalytics = (filters) => {
//   const [data, setData] = useState(null);
//   const [loading, setLoading] = useState(true);
//   const [error, setError] = useState(null);

//   useEffect(() => {
//     fetchData();
//   }, [JSON.stringify(filters)]);

//   const fetchData = async () => {
//     setLoading(true);
//     setError(null);

//     try {
//       const result = await eel.get_customer_analytics(
//         filters.dateFilter || 'all',
//         filters.startDate || null,
//         filters.endDate || null,
//         filters.quoteStatus || 'all',
//         filters.productType || 'all'
//       )();

//       if (result.success) {
//         setData(result.data);
//       } else {
//         setError(result.error || 'Failed to fetch data');
//       }
//     } catch (err) {
//       console.error('Error:', err);
//       setError('Failed to fetch data');
//     } finally {
//       setLoading(false);
//     }
//   };

//   return { data, loading, error, refetch: fetchData };
// };

// export const useCombinedInsights = (filters) => {
//   return useAnalyticsData(eel.get_combined_insights, filters);
// };

// export const exportAnalyticsData = async (view, format, filters) => {
//   try {
//     const result = await eel.export_analytics_data(
//       view,
//       format,
//       filters.dateFilter || 'all',
//       filters.startDate || null,
//       filters.endDate || null
//     )();

//     return result;
//   } catch (error) {
//     console.error('Export error:', error);
//     return { success: false, error: error.message };
//   }
// };