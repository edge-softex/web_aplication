import { configureStore } from '@reduxjs/toolkit';

import powerReducer from './reducers/powerDataSlice';
import yieldReducer from './reducers/yieldDataSlice';
import meteorologicalReducer from './reducers/meteorologicalDataSlice';
import historyReducer from './reducers/historyDataSlice';
import statusReducer from './reducers/statusDataSlice';
import pvdataHistoryReducer from './reducers/pvdataHistoryDataSlice';
import forecastHistoryReducer from './reducers/forecastHistoryDataSlice';

export default configureStore({
  reducer: {
    power: powerReducer,
    yield: yieldReducer,
    meteorological: meteorologicalReducer,
    history: historyReducer,
    status: statusReducer,
    pvdataHistory: pvdataHistoryReducer,
    forecastHistory: forecastHistoryReducer,
  },
});
