import React, { useState, useEffect } from 'react';
import PropTypes from 'prop-types';

import SmallButtonFooter from '../../atoms/SmallButtonFooter/SmallButtonFooter';

import './LisOfSmallButtonsFooter.css';

function LisOfSmallButtonsFooter(props) {
  const { pages, setPage } = props;
  const [actualPage, setActualPage] = useState(1);
  const [pageList, setPageList] = useState([1]);
  const [showBeginButton, setShowBeginButton] = useState(false);
  const [showEndButton, setShowEndButton] = useState(false);

  useEffect(() => {
    let initPage = 1;
    let endPage = pages;
    if (pages > 5) {
      initPage = actualPage - 2;
      endPage = actualPage + 2;
      if (actualPage < 3) {
        initPage = 1;
        endPage = 5;
      }
      if (actualPage > pages - 2) {
        initPage = pages - 4;
        endPage = pages;
      }
    }
    const list = [];
    for (let i = initPage; i <= endPage; i += 1) {
      list.push(i);
    }
    setPageList(list);

    setShowBeginButton(list[0] !== 1);
    setShowEndButton(list[list.length - 1] !== pages);
  }, [actualPage, pages]);

  return (
    <div className="LisOfSmallButtonsFooter_div-container">
      {showBeginButton && (
        <SmallButtonFooter
          onClick={() => {
            setPage(pageList[0] - 1);
            setActualPage(pageList[0] - 1);
          }}
          key="begin"
        >
          {'<'}
        </SmallButtonFooter>
      )}
      {pageList.map((element) => (
        <SmallButtonFooter
          onClick={() => {
            setPage(element);
            setActualPage(element);
          }}
          key={element}
          disabled={actualPage === element}
        >
          {element}
        </SmallButtonFooter>
      ))}
      {showEndButton && (
        <SmallButtonFooter
          onClick={() => {
            setPage(pageList[pageList.length - 1] + 1);
            setActualPage(pageList[pageList.length - 1] + 1);
          }}
          key="end"
        >
          {'>'}
        </SmallButtonFooter>
      )}
    </div>
  );
}

LisOfSmallButtonsFooter.propTypes = {
  pages: PropTypes.number.isRequired,
  setPage: PropTypes.func.isRequired,
};

export default LisOfSmallButtonsFooter;
