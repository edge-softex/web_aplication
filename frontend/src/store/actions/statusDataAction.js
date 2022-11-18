// eslint-disable-next-line import/no-unresolved
import axios from 'axios';
import { API_URL, API_TOKEN } from '../../network';
import { insertStatusData, isLaodingStatus, isStatusLoaded } from '../reducers/statusDataSlice';

function getStatusData() {
  const sessionURL = `${API_URL}/pvdata/status/`;

  return async (dispatch) => {
    dispatch(isLaodingStatus(true));
    dispatch(isStatusLoaded(false));

    return axios.get(sessionURL, {
      headers: {
        Authorization: `Token ${API_TOKEN}`,
      },
    }).then(({ data }) => {
      dispatch(insertStatusData(data));
      dispatch(isLaodingStatus(false));
      dispatch(isStatusLoaded(true));
    });
  };
}

export default getStatusData;
