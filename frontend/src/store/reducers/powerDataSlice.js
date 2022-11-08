import { createSlice } from '@reduxjs/toolkit';

export const powerSlice = createSlice({
  name: 'power',
  initialState: {
    powerData: {},
    auth: {
      dataLoading: false,
      dataLoaded: false,
    },
  },
  reducers: {
    insertPowerData(state, action) {
      state.powerData = action.payload;
    },
    isLaodingPower(state, action) {
      state.dataLoading = action.payload;
    },
    isPowerLoaded(state, action) {
      state.dataLoaded = action.payload;
    },
  },
});

// Action creators are generated for each case reducer function
export const {
  insertPowerData, isLaodingPower, isPowerLoaded,
} = powerSlice.actions;

export default powerSlice.reducer;
