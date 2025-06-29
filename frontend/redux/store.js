'use client'
import { combineReducers, configureStore } from '@reduxjs/toolkit';
import chatReducer from './features/chatSlice';
const rootReducer = combineReducers({
    chat: chatReducer,
});
export const store = configureStore({ reducer: rootReducer });
