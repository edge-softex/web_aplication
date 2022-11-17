import { createSlice } from '@reduxjs/toolkit';

export const meteorologicalSlice = createSlice({
  name: 'meteorological',
  initialState: {
    meteorologicalData: {
      timestamp: ['none'],
      irradiance: [0],
      temperature_pv: [0],
      temperature_amb: [0],
    },
    auth: {
      dataLoading: false,
      dataLoaded: false,
    },
  },
  reducers: {
    insertMeteorologicalData(state, action) {
      state.meteorologicalData = action.payload;
    },
    isLaodingMeteorological(state, action) {
      state.dataLoading = action.payload;
    },
    isMeteorologicalLoaded(state, action) {
      state.dataLoaded = action.payload;
    },
  },
});

// Action creators are generated for each case reducer function
export const {
  insertMeteorologicalData, isLaodingMeteorological, isMeteorologicalLoaded,
} = meteorologicalSlice.actions;

export default meteorologicalSlice.reducer;
