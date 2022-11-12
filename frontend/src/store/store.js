import { configureStore } from '@reduxjs/toolkit';

import powerReducer from './reducers/powerDataSlice';
import yieldReducer from './reducers/yieldDataSlice';

export default configureStore({
  reducer: {
    power: powerReducer,
    yield: yieldReducer,
  },
});
