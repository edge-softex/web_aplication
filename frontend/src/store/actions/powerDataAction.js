// eslint-disable-next-line import/no-unresolved
import axios from 'axios';
import { API_URL, API_TOKEN } from '../../network';
import { insertPowerData, isLaodingPower, isPowerLoaded } from '../reducers/powerDataSlice';

function getPowerData() {
  const sessionURL = `${API_URL}/pvdata/powerday/?time_interval=360`;

  return async (dispatch) => {
    dispatch(isLaodingPower(true));
    dispatch(isPowerLoaded(false));

    return axios.get(sessionURL, {
      headers: {
        Authorization: `Token ${API_TOKEN}`,
      },
    }).then(({ data }) => {
      dispatch(insertPowerData(data));
      dispatch(isLaodingPower(false));
      dispatch(isPowerLoaded(true));
    });
  };
}

export default getPowerData;
