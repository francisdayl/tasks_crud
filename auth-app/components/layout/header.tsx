"use client"

import Link from "next/link"
import { usePathname } from "next/navigation"
import { useSelector } from "react-redux"
import type { RootState } from "@/store"
import { Button } from "@/components/ui/button"
import { useAppDispatch } from "@/store/hooks"
import { logout } from "@/store/slices/auth-slice"

export default function Header() {
  const pathname = usePathname()
  const dispatch = useAppDispatch()
  const { isAuthenticated } = useSelector((state: RootState) => state.auth)

  const handleLogout = () => {
    dispatch(logout())
  }

  return (
    <header className="sticky top-0 z-50 w-full border-b bg-background">
      <div className="container flex h-16 items-center justify-between">
        <div className="flex items-center gap-6 md:gap-10">
          <Link href="/" className="flex items-center space-x-2">
            <span className="text-xl font-bold">Tasks App</span>
          </Link>
        </div>
        <nav className="flex items-center gap-4">
          {isAuthenticated ? (
            <>
              <Button asChild variant="ghost">
                <Link href="/dashboard">Dashboard</Link>
              </Button>
              <Button variant="outline" onClick={handleLogout}>
                Logout
              </Button>
            </>
          ) : (
            <>
              {pathname !== "/auth/login" && (
                <Button asChild variant="ghost">
                  <Link href="/auth/login">Login</Link>
                </Button>
              )}
              {pathname !== "/auth/register" && (
                <Button asChild variant="outline">
                  <Link href="/auth/register">Register</Link>
                </Button>
              )}
            </>
          )}
        </nav>
      </div>
    </header>
  )
}

