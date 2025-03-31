import { configureStore } from "@reduxjs/toolkit"
import authReducer from "./slices/auth-slice"

export const store = configureStore({
  reducer: {
    auth: authReducer,
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware({
      serializableCheck: {
        // Ignore these action types
        ignoredActions: ["auth/login"],
        // Ignore these field paths in all actions
        ignoredActionPaths: ["payload.user.created_at"],
        // Ignore these paths in the state
        ignoredPaths: ["auth.user.created_at"],
      },
    }),
})

export type RootState = ReturnType<typeof store.getState>
export type AppDispatch = typeof store.dispatch

