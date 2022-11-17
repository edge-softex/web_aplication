// eslint-disable-next-line import/no-unresolved
import axios from 'axios';
import { API_URL, API_TOKEN } from '../../network';
import { insertHistoryData, isLaodingHistory, isHistoryLoaded } from '../reducers/historyDataSlice';

function getHistoryData() {
  const sessionURL = `${API_URL}/yieldday/latest10/`;

  return async (dispatch) => {
    dispatch(isLaodingHistory(true));
    dispatch(isHistoryLoaded(false));

    return axios.get(sessionURL, {
      headers: {
        Authorization: `Token ${API_TOKEN}`,
      },
    }).then(({ data }) => {
      dispatch(insertHistoryData(data));
      dispatch(isLaodingHistory(false));
      dispatch(isHistoryLoaded(true));
    });
  };
}

export default getHistoryData;
