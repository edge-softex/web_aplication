import { createSlice } from '@reduxjs/toolkit';

export const statusSlice = createSlice({
  name: 'status',
  initialState: {
    statusData: {
      status: 'offline',
      status_string: 'Offline',
    },
    auth: {
      dataLoading: false,
      dataLoaded: false,
    },
  },
  reducers: {
    insertStatusData(state, action) {
      state.statusData = action.payload;
    },
    isLaodingStatus(state, action) {
      state.dataLoading = action.payload;
    },
    isStatusLoaded(state, action) {
      state.dataLoaded = action.payload;
    },
  },
});

// Action creators are generated for each case reducer function
export const {
  insertStatusData, isLaodingStatus, isStatusLoaded,
} = statusSlice.actions;

export default statusSlice.reducer;
