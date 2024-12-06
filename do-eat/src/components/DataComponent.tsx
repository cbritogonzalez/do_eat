// import { useState, useEffect } from 'react';
import apiService from '../services/apiService';
import { useApi } from '../hooks/useApi';

interface DataItem {
  id: string;
  name: string;
  // ... other properties
}

// This is an example data component, it should be replaced with the actual data component
export function DataComponent() {
  const { data, loading, error, execute: fetchData } = useApi(apiService.getData);

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;
  if (!data) return null;

  return (
    <div>
      {data.map((item: DataItem) => (
        <div key={item.id}>{item.name}</div>
      ))}
      <button onClick={() => fetchData()}>Refresh Data</button>
    </div>
  );
} 