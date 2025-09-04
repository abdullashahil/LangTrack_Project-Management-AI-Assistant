import type React from "react"
import { GeistSans } from "geist/font/sans"
import { GeistMono } from "geist/font/mono"
import { Analytics } from "@vercel/analytics/next"
import "./globals.css"
import { Topbar } from "@/components/topbar"
import { Suspense } from "react"
import { ThemeProvider } from "next-themes"


export const metadata = {
  title: "LangTrack - Project Management Assistant",
  description: "AI-powered project tracking and management system",
  icons: {
    icon: "/logo.svg",
    shortcut: "/logo.svg",
    apple: "/logo.svg",
  },
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className={`min-h-screen antialiased font-sans ${GeistSans.variable} ${GeistMono.variable}`}>
        <ThemeProvider attribute="class" defaultTheme="system" enableSystem disableTransitionOnChange>
          <div className="relative min-h-screen">
            {/* Background - subtle emerald radial glows */}
            <div aria-hidden="true" className="pointer-events-none fixed inset-0 -z-10">
              <div className="absolute inset-0 bg-background" />
              <div className="absolute inset-0 bg-gradient-to-b from-transparent to-black/10 dark:to-black/40" />
              <div className="absolute right-[-10%] top-[-10%] h-[40rem] w-[40rem] rounded-full bg-emerald-500/10 blur-3xl" />
              <div className="absolute left-[-20%] bottom-[-20%] h-[30rem] w-[30rem] rounded-full bg-emerald-400/10 blur-3xl" />
            </div>

            <Suspense fallback={<div>Loading...</div>}>
              <Topbar />
              <main className="relative mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-6">{children}</main>
            </Suspense>
          </div>
          <Analytics />
        </ThemeProvider>
      </body>
    </html>
  )
}

