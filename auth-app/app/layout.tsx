import type React from "react"
import type { Metadata } from "next"
import { Inter } from "next/font/google"
import "./globals.css"
import { Providers } from "@/store/providers"
import { ThemeProvider } from "@/components/theme-provider"
import Header from "@/components/layout/header"

const inter = Inter({ subsets: ["latin"] })

export const metadata: Metadata = {
  title: "Authentication App",
  description: "Next.js 15 Authentication Application",
    generator: 'v0.dev'
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <ThemeProvider attribute="class" defaultTheme="system" enableSystem disableTransitionOnChange>
          <Providers>
            <div className="flex min-h-screen flex-col">
              <Header />
              <main className="flex-1">{children}</main>
            </div>
          </Providers>
        </ThemeProvider>
      </body>
    </html>
  )
}



import './globals.css'