"use client"

import { useState, useEffect } from "react"
import { getUserTasks } from "@/lib/tasks"
import type { Task } from "@/types"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Skeleton } from "@/components/ui/skeleton"
import { CalendarIcon, ClockIcon } from "lucide-react"

export default function TaskList() {
  const [tasks, setTasks] = useState<Task[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchTasks = async () => {
      try {
        const response = await getUserTasks()
        setTasks(response.data)
      } catch (err) {
        setError(err instanceof Error ? err.message : "Failed to fetch tasks")
      } finally {
        setIsLoading(false)
      }
    }

    fetchTasks()
  }, [])

  if (isLoading) {
    return (
      <div className="space-y-4">
        {[1, 2, 3].map((i) => (
          <Card key={i}>
            <CardHeader className="pb-2">
              <Skeleton className="h-5 w-1/3" />
              <Skeleton className="h-4 w-1/4" />
            </CardHeader>
            <CardContent>
              <Skeleton className="h-4 w-full mb-2" />
              <Skeleton className="h-4 w-2/3" />
            </CardContent>
          </Card>
        ))}
      </div>
    )
  }

  if (error) {
    return (
      <Card className="border-destructive">
        <CardHeader>
          <CardTitle>Error</CardTitle>
          <CardDescription>Failed to load tasks</CardDescription>
        </CardHeader>
        <CardContent>
          <p>{error}</p>
        </CardContent>
      </Card>
    )
  }

  if (tasks.length === 0) {
    return (
      <Card>
        <CardHeader>
          <CardTitle>No Tasks</CardTitle>
          <CardDescription>You don't have any tasks yet</CardDescription>
        </CardHeader>
        <CardContent>
          <p>Create a new task to get started.</p>
        </CardContent>
      </Card>
    )
  }

  const getStatusColor = (status: string) => {
    switch (status.toLowerCase()) {
      case "pendiente":
        return "bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-300"
      case "en progreso":
        return "bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-300"
      case "completado":
        return "bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300"
      default:
        return "bg-gray-100 text-gray-800 dark:bg-gray-800 dark:text-gray-300"
    }
  }

  const formatDate = (dateString: string) => {
    const date = new Date(dateString)
    return date.toLocaleDateString("en-US", {
      year: "numeric",
      month: "short",
      day: "numeric",
    })
  }

  return (
    <div className="space-y-4">
      {tasks.map((task) => (
        <Card key={task.id} className="overflow-hidden">
          <CardHeader className="pb-2">
            <div className="flex justify-between items-start">
              <div>
                <CardTitle className="text-lg">{task.title}</CardTitle>
                <CardDescription className="text-sm mt-1">{task.description}</CardDescription>
              </div>
              <Badge className={getStatusColor(task.status)}>{task.status}</Badge>
            </div>
          </CardHeader>
          <CardContent>
            <div className="flex flex-wrap gap-4 text-sm text-muted-foreground">
              <div className="flex items-center">
                <CalendarIcon className="mr-1 h-3 w-3" />
                <span>Created: {formatDate(task.created_at)}</span>
              </div>
              <div className="flex items-center">
                <ClockIcon className="mr-1 h-3 w-3" />
                <span>Updated: {formatDate(task.updated_at)}</span>
              </div>
            </div>
          </CardContent>
        </Card>
      ))}
    </div>
  )
}

