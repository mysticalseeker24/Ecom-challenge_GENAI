'use client'
import { createSlice } from '@reduxjs/toolkit';

const initialState = {
    value: {
        messages: [],
    }
};

const getLocalStorage = (name) => {
    if (typeof window !== 'undefined') {
        try {
            const stored = window.localStorage.getItem(name);
            const parsed = JSON.parse(stored);
            if (parsed?.value?.messages && Array.isArray(parsed.value.messages)) {
                return parsed;
            }
        } catch (e) {}
    }
    return initialState;
};

const setLocalStorage = (name, value) => {
    if (typeof window !== 'undefined') {
        window.localStorage.setItem(name, JSON.stringify(value));
    }
};

export const chat = createSlice({
    name: "chat",
    initialState: typeof window !== 'undefined' ? getLocalStorage('chatState') : initialState,
    reducers: {
        clear: () => {
            setLocalStorage('chatState', initialState);
            return initialState;
        },
        addMessage: (state, action) => {
            const updatedMessages = [...state.value.messages, action.payload];
            const newState = {
                value: {
                    messages: updatedMessages
                }
            };
            setLocalStorage('chatState', newState);
            return newState;
        }
    },
});

export const { clear, addMessage } = chat.actions;
export default chat.reducer;
