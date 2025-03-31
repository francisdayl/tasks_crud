import { createSlice, type PayloadAction } from "@reduxjs/toolkit"
import type { AuthResponse, User } from "@/types"
import {
  getAuthToken,
  getUserFromStorage,
  removeAuthToken,
  removeUserFromStorage,
  setAuthToken,
  setUserInStorage,
} from "@/lib/auth"

interface AuthState {
  user: User | null
  token: string | null
  isAuthenticated: boolean
  expiresIn: number | null
}

const initialState: AuthState = {
  user: getUserFromStorage(),
  token: getAuthToken(),
  isAuthenticated: !!getAuthToken(),
  expiresIn: null,
}

const authSlice = createSlice({
  name: "auth",
  initialState,
  reducers: {
    login: (state, action: PayloadAction<AuthResponse>) => {
      state.user = action.payload.data.user
      state.token = action.payload.data.token
      state.isAuthenticated = true
      state.expiresIn = action.payload.data.expires_in
      // Store in localStorage
      setAuthToken(action.payload.data.token)
      setUserInStorage(action.payload.data.user)
    },
    logout: (state) => {
      state.user = null
      state.token = null
      state.isAuthenticated = false
      state.expiresIn = null

      // Remove from localStorage
      removeAuthToken()
      removeUserFromStorage()
    },
  },
})

export const { login, logout } = authSlice.actions
export default authSlice.reducer

