import React from 'react';
import PropTypes from 'prop-types';

import SmallButtonFooter from '../../atoms/SmallButtonFooter/SmallButtonFooter';

import './LisOfSmallButtonsFooter.css';

function LisOfSmallButtonsFooter(props) {
  const { list } = props;

  return (
    <div className="LisOfSmallButtonsFooter_div-container">
      {list.map((element) => <SmallButtonFooter>{element}</SmallButtonFooter>)}
    </div>
  );
}

LisOfSmallButtonsFooter.propTypes = {
  list: PropTypes.arrayOf(
    PropTypes.number,
  ).isRequired,
};

export default LisOfSmallButtonsFooter;
