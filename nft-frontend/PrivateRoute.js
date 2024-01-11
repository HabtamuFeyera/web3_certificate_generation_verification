import React, { useContext } from 'react';
import { Route, Redirect } from 'react-router-dom';
import { AuthContext } from '../contexts/AuthContext';

function PrivateRoute({ component: Component, staffOnly, publicOnly, ...rest }) {
  const { currentUser } = useContext(AuthContext);

  if (staffOnly && (!currentUser || !currentUser.isStaff)) {
    return <Redirect to="/" />;
  }

  if (publicOnly && (!currentUser || currentUser.isStaff)) {
    return <Redirect to="/" />;
  }

  return <Route {...rest} render={(props) => <Component {...props} />} />;
}

export default PrivateRoute;
