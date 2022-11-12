// eslint-disable-next-line import/no-unresolved
import axios from 'axios';
import { API_URL, API_TOKEN } from '../../network';
import { insertYieldData, isLaodingYield, isYieldLoaded } from '../reducers/yieldDataSlice';

function getYieldData() {
  const sessionURL = `${API_URL}/yieldminute/today/`;

  return async (dispatch) => {
    dispatch(isLaodingYield(true));
    dispatch(isYieldLoaded(false));

    return axios.get(sessionURL, {
      headers: {
        Authorization: `Token ${API_TOKEN}`,
      },
    }).then(({ data }) => {
      dispatch(insertYieldData(data));
      dispatch(isLaodingYield(false));
      dispatch(isYieldLoaded(true));
    });
  };
}

export default getYieldData;
