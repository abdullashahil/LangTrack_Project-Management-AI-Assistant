"use client"

import Link from "next/link"
import { MessageCircle } from "lucide-react"
import { ThemeToggle } from "./theme-toggle"

export function Topbar() {
  return (
    <header className="sticky top-0 z-20 w-full border-b border-white/10 bg-white/60 backdrop-blur supports-[backdrop-filter]:bg-white/60 dark:bg-black/30">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 h-14 flex items-center justify-between">
        <Link href="/" className="flex items-center gap-2" aria-label="Go to home">
          <span className="inline-flex h-8 w-8 items-center justify-center rounded-lg bg-emerald-500 text-black">
            <MessageCircle className="h-5 w-5" aria-hidden="true" />
          </span>
          <span className="font-semibold tracking-tight text-foreground">LangTrack</span>
        </Link>

        <div className="flex items-center gap-2">
          <ThemeToggle />
        </div>
      </div>
    </header>
  )
}
