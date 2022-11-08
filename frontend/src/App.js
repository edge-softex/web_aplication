import React from 'react';
import { Routes, Route } from 'react-router-dom';

import './App.css';

import Dashboard from './containers/Dashboard/Dashboard';
import Layout from './HighOrderComponents/Layout/Layout';
import Historic from './containers/Historic/Historic';
import Settings from './containers/Settings/Settings';

function App() {
  return (
    <div className="App">
      <Layout>
        <Routes>
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/history" element={<Historic />} />
          <Route path="/settings" element={<Settings />} />
        </Routes>
      </Layout>
    </div>
  );
}

export default App;
