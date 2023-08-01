// eslint-disable-next-line import/no-unresolved
import axios from 'axios';
import { API_URL, API_TOKEN } from '../../network';
import { insertForecast, isLaodingForecast, isForecastLoaded } from '../reducers/forecastHistoryDataSlice';

function getForecast(page, beginTime, endTime) {
  let sessionURL = `${API_URL}/powerforecast/history/?page=${page}`;

  if (beginTime !== '') {
    sessionURL += `&time_begin=${beginTime}`;
  }

  if (endTime !== '') {
    sessionURL += `&time_end=${endTime}`;
  }

  return async (dispatch) => {
    dispatch(isLaodingForecast(true));
    dispatch(isForecastLoaded(false));

    return axios.get(sessionURL, {
      headers: {
        'ngrok-skip-browser-warning': 'true',
        Authorization: `Token ${API_TOKEN}`,
      },
    }).then(({ data }) => {
      dispatch(insertForecast(data));
      dispatch(isLaodingForecast(false));
      dispatch(isForecastLoaded(true));
    });
  };
}

export default getForecast;
