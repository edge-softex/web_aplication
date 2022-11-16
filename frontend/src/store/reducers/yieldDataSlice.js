import { createSlice } from '@reduxjs/toolkit';

export const yieldSlice = createSlice({
  name: 'yield',
  initialState: {
    yieldData: {
      timestamp: ['none'],
      data: [0],
    },
    auth: {
      dataLoading: false,
      dataLoaded: false,
    },
  },
  reducers: {
    insertYieldData(state, action) {
      state.yieldData = action.payload;
    },
    isLaodingYield(state, action) {
      state.dataLoading = action.payload;
    },
    isYieldLoaded(state, action) {
      state.dataLoaded = action.payload;
    },
  },
});

// Action creators are generated for each case reducer function
export const {
  insertYieldData, isLaodingYield, isYieldLoaded,
} = yieldSlice.actions;

export default yieldSlice.reducer;
