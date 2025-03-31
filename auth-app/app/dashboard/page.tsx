"use client"

import { useEffect } from "react"
import { useRouter } from "next/navigation"
import { useSelector } from "react-redux"
import type { RootState } from "@/store"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { useAppDispatch } from "@/store/hooks"
import { logout } from "@/store/slices/auth-slice"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import TaskList from "@/components/dashboard/tasks-list"

export default function DashboardPage() {
  const router = useRouter()
  const dispatch = useAppDispatch()
  const { user, isAuthenticated } = useSelector((state: RootState) => state.auth)

  useEffect(() => {
    if (!isAuthenticated) {
      router.push("/auth/login")
    }
  }, [isAuthenticated, router])

  const handleLogout = () => {
    dispatch(logout())
    router.push("/auth/login")
  }

  if (!isAuthenticated || !user) {
    return null
  }

  return (
    <div className="container py-10">
      <h1 className="mb-6 text-3xl font-bold">Dashboard</h1>

      <Tabs defaultValue="tasks" className="mb-8">
        <TabsList>
          <TabsTrigger value="tasks">My Tasks</TabsTrigger>
          <TabsTrigger value="profile">Profile</TabsTrigger>
        </TabsList>

        <TabsContent value="tasks" className="mt-6">
          <div className="mb-6">
            <h2 className="text-2xl font-semibold mb-2">Your Tasks</h2>
            <p className="text-muted-foreground">Manage your tasks and track your progress</p>
          </div>
          <TaskList />
        </TabsContent>

        <TabsContent value="profile">
          <div className="grid gap-6 md:grid-cols-2">
            <Card>
              <CardHeader>
                <CardTitle>User Information</CardTitle>
                <CardDescription>Your account details</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-2">
                  <div className="flex justify-between">
                    <span className="font-medium">Email:</span>
                    <span>{user.email}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="font-medium">Created At:</span>
                    <span>{new Date(user.created_at.$date).toLocaleDateString()}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="font-medium">Status:</span>
                    <span className={user.is_active ? "text-green-500" : "text-red-500"}>
                      {user.is_active ? "Active" : "Inactive"}
                    </span>
                  </div>
                </div>
              </CardContent>
            </Card>
            <Card>
              <CardHeader>
                <CardTitle>Account Actions</CardTitle>
                <CardDescription>Manage your account</CardDescription>
              </CardHeader>
              <CardContent>
                <Button variant="destructive" onClick={handleLogout}>
                  Logout
                </Button>
              </CardContent>
            </Card>
          </div>
        </TabsContent>
      </Tabs>
    </div>
  )
}

