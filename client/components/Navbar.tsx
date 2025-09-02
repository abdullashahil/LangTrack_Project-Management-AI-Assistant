"use client";

import Link from "next/link";
import { MessageCircle } from "lucide-react";

export function Navbar() {

  return (
    <nav className="bg-white dark:bg-gray-900 w-full border-b border-gray-200 dark:border-gray-800">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">

          {/* Logo/Title - Centered */}
          <div className="flex-1 flex items-center justify-center md:justify-center">
          <Link href="/" className="flex items-center gap-2">
            <MessageCircle className="h-8 w-8 text-blue-600" />
            <span className="text-xl font-bold text-gray-900">LangTrack</span>
          </Link>
          </div>

          <div className="hidden md:block w-6"></div>
        </div>
      </div>

    </nav>
  );
}