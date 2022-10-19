import { insertPowerData, isLaodingPower, isPowerLoaded } from '../reducers/powerDataSlice';

export function getPowerData() {
  return async (dispatch) => {
    dispatch(isLaodingPower(false));
    dispatch(isPowerLoaded(false));
    return dispatch(insertPowerData(
      { data: [1, 2, 3, 4, 5] },
      { label: [1, 2, 3, 4, 5] },
    ));
  };
}

export function teste() {}
