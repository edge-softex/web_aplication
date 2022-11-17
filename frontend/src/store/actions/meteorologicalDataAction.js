// eslint-disable-next-line import/no-unresolved
import axios from 'axios';
import { API_URL, API_TOKEN } from '../../network';
import { insertMeteorologicalData, isLaodingMeteorological, isMeteorologicalLoaded } from '../reducers/meteorologicalDataSlice';

function getMeteorologicalData() {
  const sessionURL = `${API_URL}/pvdata/meteorologicalday/`;

  return async (dispatch) => {
    dispatch(isLaodingMeteorological(true));
    dispatch(isMeteorologicalLoaded(false));

    return axios.get(sessionURL, {
      headers: {
        Authorization: `Token ${API_TOKEN}`,
      },
    }).then(({ data }) => {
      dispatch(insertMeteorologicalData(data));
      dispatch(isLaodingMeteorological(false));
      dispatch(isMeteorologicalLoaded(true));
    });
  };
}

export default getMeteorologicalData;
