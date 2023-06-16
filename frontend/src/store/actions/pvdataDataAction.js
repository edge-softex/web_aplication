// eslint-disable-next-line import/no-unresolved
import axios from 'axios';
import { API_URL, API_TOKEN } from '../../network';
import { insertPvData, isLaodingPvData, isPvDataLoaded } from '../reducers/pvdataHistoryDataSlice';

function getPvData(page) {
  const sessionURL = `${API_URL}/pvdata/history/?page=${page}`;

  return async (dispatch) => {
    dispatch(isLaodingPvData(true));
    dispatch(isPvDataLoaded(false));

    return axios.get(sessionURL, {
      headers: {
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
