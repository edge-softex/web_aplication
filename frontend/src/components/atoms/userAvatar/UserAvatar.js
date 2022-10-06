import React from 'react';
import PropTypes from 'prop-types';

import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faCircleUser } from '@fortawesome/free-solid-svg-icons';

import './UserAvatar.css';

function UserAvatar(props) {
  const { name } = props;

  return (
    <div className="userAvatar_div-container">
      <FontAwesomeIcon icon={faCircleUser} />
      <p className="userAvatar_p">{name}</p>
    </div>
  );
}

UserAvatar.propTypes = {
  name: PropTypes.string.isRequired,
};

export default UserAvatar;
