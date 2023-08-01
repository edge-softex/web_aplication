import React from 'react';
import PropTypes from 'prop-types';

import LisOfSmallButtonsFooter from '../../Molecules/ListOfSmallButtonsFooter/LisOfSmallButtonsFooter';

import './FooterHistoric.css';

function FooterHistoric(props) {
  const {
    pages,
    setPage,
    historyPage,
    elements,
    dataset,
  } = props;

  // setPage(1);

  return (
    <div className="FooterHistoric_div-container">
      <p>
        {`${elements} de ${dataset} registros`}
      </p>
      <LisOfSmallButtonsFooter pages={pages} setPage={setPage} historyPage={historyPage} />
    </div>
  );
}

FooterHistoric.propTypes = {
  setPage: PropTypes.func.isRequired,
  pages: PropTypes.number.isRequired,
  historyPage: PropTypes.number.isRequired,
  elements: PropTypes.number.isRequired,
  dataset: PropTypes.number.isRequired,
};

export default FooterHistoric;
