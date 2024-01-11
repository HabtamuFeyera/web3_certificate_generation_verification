import React from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import { AuthProvider } from './contexts/AuthContext';
import PrivateRoute from './components/PrivateRoute';
import Home from './components/Home';
import StaffDashboard from './components/StaffDashboard';
import TraineeDashboard from './components/TraineeDashboard';
import PublicDashboard from './components/PublicDashboard';

function App() {
  return (
    <Router>
      <AuthProvider>
        <Switch>
          <Route path="/" exact component={Home} />
          <PrivateRoute path="/staff-dashboard" component={StaffDashboard} staffOnly />
          <PrivateRoute path="/trainee-dashboard" component={TraineeDashboard} />
          <PrivateRoute path="/public-dashboard" component={PublicDashboard} publicOnly />
        </Switch>
      </AuthProvider>
    </Router>
  );
}

export default App;
