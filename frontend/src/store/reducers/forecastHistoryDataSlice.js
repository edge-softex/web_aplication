import { createSlice } from '@reduxjs/toolkit';

export const forecastHistorySlice = createSlice({
  name: 'forecastHistory',
  initialState: {
    forecast: {
      pages: 1,
      dataset: 0,
      timestamp: ['none'],
      power_avg: [0],
      t1: [0],
      t2: [0],
      t3: [0],
      t4: [0],
      t5: [0],
    },
    auth: {
      dataLoading: false,
      dataLoaded: false,
    },
  },
  reducers: {
    insertForecast(state, action) {
      state.forecast = action.payload;
    },
    isLaodingForecast(state, action) {
      state.dataLoading = action.payload;
    },
    isForecastLoaded(state, action) {
      state.dataLoaded = action.payload;
    },
  },
});

// Action creators are generated for each case reducer function
export const {
  insertForecast, isLaodingForecast, isForecastLoaded,
} = forecastHistorySlice.actions;

export default forecastHistorySlice.reducer;
