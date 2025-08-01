import type React from "react"
import { Navbar } from "@/components/Navbar"
import "./globals.css"
import { Inter } from "next/font/google"

const inter = Inter({ subsets: ["latin"] })

export const metadata = {
  title: "LangTrack - Project Management Assistant",
  description: "AI-powered project tracking and management system",
  icons: {
    icon: "/logo.png",
    shortcut: "/logo.png",
    apple: "/logo.png",
  },
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className={`${inter.className} overflow-hidden`}>
        <Navbar />
        <main className="h-[calc(100vh-64px)] bg-gray-50/50">{children}</main>
      </body>
    </html>
  )
}
