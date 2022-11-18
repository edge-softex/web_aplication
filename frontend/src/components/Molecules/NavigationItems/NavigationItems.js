import React, { useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';

import getStatusData from '../../../store/actions/statusDataAction';

import SystemStatus from '../../atoms/SystemStatus/SystemStatus';
import UserAvatar from '../../atoms/userAvatar/UserAvatar';

import './NavigationItems.css';

function NavigationItems() {
  const statusData = useSelector((state) => state.status.statusData);
  const dispatch = useDispatch();

  useEffect(() => {
    dispatch(getStatusData());
  }, []);

  useEffect(() => {
    const interval = setInterval(() => {
      dispatch(getStatusData());
    }, 5000);
    return () => clearInterval(interval);
  }, []);

  return (
    <ul className="nav_list">
      <li>
        <SystemStatus
          status={statusData.status}
          statusString={statusData.status_string}
        />
      </li>
      <li>
        <UserAvatar name="Vinicius Feitosa" />
      </li>
    </ul>
  );
}

export default NavigationItems;
