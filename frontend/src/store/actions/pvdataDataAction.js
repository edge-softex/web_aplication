// eslint-disable-next-line import/no-unresolved
import axios from 'axios';
import { API_URL, API_TOKEN } from '../../network';
import { insertPvData, isLaodingPvData, isPvDataLoaded } from '../reducers/pvdataHistoryDataSlice';

function getPvData(page, beginTime, endTime) {
  let sessionURL = `${API_URL}/pvdata/history/?page=${page}`;

  if (beginTime !== '') {
    sessionURL += `&time_begin=${beginTime}`;
  }

  if (endTime !== '') {
    sessionURL += `&time_end=${endTime}`;
  }

  return async (dispatch) => {
    dispatch(isLaodingPvData(true));
    dispatch(isPvDataLoaded(false));

    return axios.get(sessionURL, {
      headers: {
        'ngrok-skip-browser-warning': 'true',
        'Bypass-Tunnel-Reminder': 'true',
        Authorization: `Token ${API_TOKEN}`,
      },
    }).then(({ data }) => {
      dispatch(insertPvData(data));
      dispatch(isLaodingPvData(false));
      dispatch(isPvDataLoaded(true));
    });
  };
}

export default getPvData;
