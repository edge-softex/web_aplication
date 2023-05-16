import { createSlice } from '@reduxjs/toolkit';

export const pvdataHistorySlice = createSlice({
  name: 'pvdataHistory',
  initialState: {
    pvData: {
      timestamp: ['none'],
      irradiance: [0],
      temperature_pv: [0],
      temperature_amb: [0],
      humidity: [0],
      wind_speed: [0],
      wind_direction: ['none'],
      rain: [0],
      open_circuit_voltage: [0],
      short_circuit_current: [0],
      power_avg: [0],
    },
    auth: {
      dataLoading: false,
      dataLoaded: false,
    },
  },
  reducers: {
    insertPvData(state, action) {
      state.pvData = action.payload;
    },
    isLaodingPvData(state, action) {
      state.dataLoading = action.payload;
    },
    isPvDataLoaded(state, action) {
      state.dataLoaded = action.payload;
    },
  },
});

// Action creators are generated for each case reducer function
export const {
  insertPvData, isLaodingPvData, isPvDataLoaded,
} = pvdataHistorySlice.actions;

export default pvdataHistorySlice.reducer;
