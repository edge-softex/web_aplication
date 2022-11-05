import axios from 'axios';
import { API_URL, API_TOKEN } from '../../network';
import { insertPowerData, isLaodingPower, isPowerLoaded } from '../reducers/powerDataSlice';

export function getPowerData() {
  const sessionURL = `${API_URL}/pvdata/powerday/`;

  return async (dispatch) => {
    dispatch(isLaodingPower(false));
    dispatch(isPowerLoaded(false));

    return axios.get(sessionURL, {
      headers: {
        Authorization: `Token ${API_TOKEN}`,
      },
    }).then(({ data }) => {
      console.log('Authenticated');
      dispatch(insertPowerData(data));
    });

    // { data: [1, 2, 3, 4, 5] },
    // { label: [1, 2, 3, 4, 5] },
  };
}

export function teste() {}
