import { configureStore } from '@reduxjs/toolkit';

import powerReducer from './reducers/powerDataSlice';

export default configureStore({
  reducer: {
    power: powerReducer,
  },
});
