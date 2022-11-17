import { configureStore } from '@reduxjs/toolkit';

import powerReducer from './reducers/powerDataSlice';
import yieldReducer from './reducers/yieldDataSlice';
import meteorologicalReducer from './reducers/meteorologicalDataSlice';
import historyReducer from './reducers/historyDataSlice';

export default configureStore({
  reducer: {
    power: powerReducer,
    yield: yieldReducer,
    meteorological: meteorologicalReducer,
    history: historyReducer,
  },
});
