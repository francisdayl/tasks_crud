export interface User {
  email: string
  created_at: {
    $date: string
  }
  is_active: boolean
}

export interface AuthPayloadResponse{
  message: string
  user: User
  token: string
  expires_in: number
}
export interface AuthResponse {
  data:AuthPayloadResponse,
  status: number,
  headers: any
}

export interface Task {
  title: string
  description: string
  status: string
  id: string
  created_at: string
  updated_at: string
  user_id: string
}

export interface TasksResponse {
  data: Task[]
}
