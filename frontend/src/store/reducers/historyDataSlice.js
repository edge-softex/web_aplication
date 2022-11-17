import { createSlice } from '@reduxjs/toolkit';

export const historySlice = createSlice({
  name: 'history',
  initialState: {
    historyData: {
      timestamp: ['none'],
      data: [0],
    },
    auth: {
      dataLoading: false,
      dataLoaded: false,
    },
  },
  reducers: {
    insertHistoryData(state, action) {
      state.historyData = action.payload;
    },
    isLaodingHistory(state, action) {
      state.dataLoading = action.payload;
    },
    isHistoryLoaded(state, action) {
      state.dataLoaded = action.payload;
    },
  },
});

// Action creators are generated for each case reducer function
export const {
  insertHistoryData, isLaodingHistory, isHistoryLoaded,
} = historySlice.actions;

export default historySlice.reducer;
