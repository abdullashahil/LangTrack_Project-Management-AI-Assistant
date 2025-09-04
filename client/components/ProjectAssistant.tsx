"use client"

import type React from "react"

import { useState, useRef, useEffect } from "react"
import { Button } from "./ui/button"
import { Card, CardHeader, CardTitle } from "./ui/card"
import { ScrollArea } from "./ui/scroll-area"
import { Send, MessageCircle, Keyboard } from "lucide-react"

interface Message {
  id: string
  type: "user" | "assistant"
  content: string
}

interface AssistantResponse {
  success: boolean
  data?: {
    answer: string
    formatted?: boolean
  }
  error?: {
    message: string
  }
}

export function ProjectAssistant() {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: "1",
      type: "assistant",
      content: "Hello! I'm your project assistant. How can I help you today?",
    },
  ])
  const [currentMessage, setCurrentMessage] = useState("")
  const [loading, setLoading] = useState(false)
  const [showShortcuts, setShowShortcuts] = useState(false)
  const scrollAreaRef = useRef<HTMLDivElement>(null)
  const bottomRef = useRef<HTMLDivElement | null>(null)
  const inputRef = useRef<HTMLTextAreaElement>(null)

  const scrollToBottom = (smooth = true) => {
    if (bottomRef.current) {
      bottomRef.current.scrollIntoView({ behavior: smooth ? "smooth" : "auto", block: "end" })
      return
    }
    if (scrollAreaRef.current) {
      const scrollContainer = scrollAreaRef.current.querySelector(
        "[data-radix-scroll-area-viewport]",
      ) as HTMLElement | null
      if (scrollContainer) {
        requestAnimationFrame(() => {
          scrollContainer.scrollTop = scrollContainer.scrollHeight
        })
      }
    }
  }

  const renderMarkdown = (text: string) => {
    return text.split("\n").map((line, i) => {
      if (line.trim().startsWith("* ")) {
        const content = line.replace(/^\s*\*\s*/, "")
        return (
          <div key={i} className="flex items-start gap-2 my-1">
            <span className="text-zinc-500 dark:text-zinc-400 mt-1">•</span>
            <span dangerouslySetInnerHTML={{ __html: formatBoldText(content) }} />
          </div>
        )
      }
      if (line.trim()) {
        return <p key={i} className="my-1 text-pretty" dangerouslySetInnerHTML={{ __html: formatBoldText(line) }} />
      }
      return <br key={i} />
    })
  }

  const formatBoldText = (text: string) => {
    return text.replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>")
  }

  useEffect(() => {
    const id = setTimeout(() => scrollToBottom(), 0)
    return () => clearTimeout(id)
  }, [messages, loading])

  useEffect(() => {
    const handleGlobalKeyDown = (e: KeyboardEvent) => {
      // Focus input when '/' is pressed (unless already focused on an input)
      if (
        e.key === "/" &&
        document.activeElement?.tagName !== "INPUT" &&
        document.activeElement?.tagName !== "TEXTAREA"
      ) {
        e.preventDefault()
        inputRef.current?.focus()
      }

      // Show shortcuts when Ctrl/Cmd + K is pressed
      if ((e.ctrlKey || e.metaKey) && e.key === "k") {
        e.preventDefault()
        setShowShortcuts((prev) => !prev)
      }

      // Escape to clear input or hide shortcuts
      if (e.key === "Escape") {
        if (showShortcuts) {
          setShowShortcuts(false)
        } else if (document.activeElement === inputRef.current) {
          setCurrentMessage("")
          inputRef.current?.blur()
        }
      }
    }

    document.addEventListener("keydown", handleGlobalKeyDown)
    return () => document.removeEventListener("keydown", handleGlobalKeyDown)
  }, [showShortcuts])

  const handleSubmit = async () => {
    const question = currentMessage.trim()
    if (!question) return

    const userMessage: Message = {
      id: Date.now().toString(),
      type: "user",
      content: question,
    }

    setMessages((prev) => [...prev, userMessage])
    setCurrentMessage("")
    setLoading(true)

    try {
      const res = await fetch("/api/ask", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question }),
      })
      const data: AssistantResponse = await res.json()

      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        type: "assistant",
        content: data.success
          ? data.data?.answer || "I couldn't process that request."
          : data.error?.message || "Something went wrong.",
      }

      setMessages((prev) => [...prev, assistantMessage])
    } catch {
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        type: "assistant",
        content: "I'm having trouble connecting right now. Please try again.",
      }
      setMessages((prev) => [...prev, errorMessage])
    } finally {
      setLoading(false)
    }
  }

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault()
      handleSubmit()
    }
    if (e.key === "Enter" && e.shiftKey) {
      // Allow default behavior for new line
      return
    }
  }

  return (
    <div className="w-full max-w-4xl mx-auto h-full max-h-[calc(100vh-160px)] relative">
      <Card className="h-full flex flex-col rounded-3xl border border-white/10 bg-white/70 backdrop-blur md:bg-white/60 dark:bg-zinc-900/60 shadow-[0_10px_40px_-15px_rgba(0,0,0,0.5)]">
        {/* Header */}
        <CardHeader className="border-b border-white/10 flex-shrink-0 py-4 bg-transparent">
          <CardTitle className="flex items-center justify-between text-lg">
            <div className="flex items-center gap-2">
              <span className="inline-flex h-7 w-7 items-center justify-center rounded-md bg-emerald-500 text-black">
                <MessageCircle className="h-4 w-4" />
              </span>
              <span className="text-foreground">Project Assistant</span>
            </div>
            <Button
              variant="ghost"
              size="sm"
              onClick={() => setShowShortcuts(!showShortcuts)}
              className="h-7 w-7 p-0 text-muted-foreground hover:text-foreground cursor-pointer transition"
            >
              <Keyboard className="h-4 w-4" />
            </Button>
          </CardTitle>
        </CardHeader>

        {/* Messages Area */}
        <div className="flex flex-col">
          <ScrollArea ref={scrollAreaRef} className="bg-transparent h-96 md:h-[24rem]">
            <div className="p-4 space-y-4">
              {messages.map((message) => (
                <div key={message.id} className={`flex ${message.type === "user" ? "justify-end" : "justify-start"}`}>
                  <div
                    className={`max-w-[85%] rounded-2xl px-4 py-3 text-sm leading-relaxed
                    ${
                      message.type === "user"
                        ? "bg-emerald-500 text-black"
                        : "bg-zinc-100 text-zinc-900 dark:bg-zinc-800/80 dark:text-zinc-100"
                    }`}
                  >
                    {message.type === "assistant" ? (
                      <div className="space-y-1">{renderMarkdown(message.content)}</div>
                    ) : (
                      <p>{message.content}</p>
                    )}
                  </div>
                </div>
              ))}

              {loading && (
                <div className="flex justify-start">
                  <div className="bg-zinc-100 text-zinc-600 dark:bg-zinc-800/80 dark:text-zinc-300 rounded-2xl px-4 py-3 text-sm">
                    <div className="flex items-center gap-2">
                      <div className="flex space-x-1">
                        <div className="w-2 h-2 bg-current rounded-full animate-bounce [animation-delay:-0.3s]"></div>
                        <div className="w-2 h-2 bg-current rounded-full animate-bounce [animation-delay:-0.15s]"></div>
                        <div className="w-2 h-2 bg-current rounded-full animate-bounce"></div>
                      </div>
                    </div>
                  </div>
                </div>
              )}

              <div ref={bottomRef} className="h-px" />
            </div>
          </ScrollArea>

          {/* Input Area */}
          <div className="border-t border-white/10 bg-transparent flex-shrink-0">
            <div className="p-4">
              <div className="flex gap-3 items-center">
                <div className="flex-1 relative mt-1">
                  <textarea
                    ref={inputRef}
                    value={currentMessage}
                    onChange={(e) => setCurrentMessage(e.target.value)}
                    onKeyDown={handleKeyDown}
                    placeholder="Type your prompt here... (Press / to focus, Enter to send)"
                    disabled={loading}
                    rows={1}
                    className="w-full min-h-[44px] max-h-32 resize-none rounded-xl bg-white/70 dark:bg-zinc-900/60 border border-white/20 placeholder:text-muted-foreground pr-20 px-3 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-transparent transition-all"
                    style={{
                      height: "auto",
                    }}
                    onInput={(e) => {
                      const target = e.target as HTMLTextAreaElement
                      target.style.height = "auto"
                      target.style.height = Math.min(target.scrollHeight, 128) + "px"
                    }}
                  />
                  <div className="absolute right-3 top-3 text-xs text-muted-foreground">
                    {currentMessage.length > 0 && <span className="mr-2">{currentMessage.length}</span>}
                    <kbd className="px-1.5 py-0.5 text-xs bg-muted rounded">⏎</kbd>
                  </div>
                </div>
                <Button
                  onClick={handleSubmit}
                  disabled={loading || !currentMessage.trim()}
                  className="h-11 px-4 rounded-xl bg-emerald-500 hover:bg-emerald-400 text-black flex items-center justify-center cursor-pointer transition disabled:opacity-50 flex-shrink-0"
                >
                  <Send className="h-4 w-4" />
                </Button>
              </div>
              <p className="text-xs text-muted-foreground mt-2 text-center">
                Press <kbd className="px-1 py-0.5 bg-muted rounded text-xs">Shift + Enter</kbd> for new line
              </p>
            </div>
          </div>
        </div>
      </Card>

      {showShortcuts && (
        <div className="absolute inset-0 bg-black/20 backdrop-blur-sm rounded-3xl flex items-center justify-center z-10">
          <Card className="p-6 w-full max-w-md mx-4 bg-white dark:bg-zinc-900 shadow-xl">
            <CardHeader className="p-0 pb-4">
              <CardTitle className="text-lg">Keyboard Shortcuts</CardTitle>
            </CardHeader>
            <div className="space-y-3 text-sm">
              <div className="flex justify-between items-center">
                <span>Focus input</span>
                <kbd className="px-2 py-1 bg-muted rounded text-xs">/</kbd>
              </div>
              <div className="flex justify-between items-center">
                <span>Send message</span>
                <kbd className="px-2 py-1 bg-muted rounded text-xs">Enter</kbd>
              </div>
              <div className="flex justify-between items-center">
                <span>New line</span>
                <kbd className="px-2 py-1 bg-muted rounded text-xs">Shift + Enter</kbd>
              </div>
              <div className="flex justify-between items-center">
                <span>Clear input</span>
                <kbd className="px-2 py-1 bg-muted rounded text-xs">Esc</kbd>
              </div>
              <div className="flex justify-between items-center">
                <span>Toggle shortcuts</span>
                <kbd className="px-2 py-1 bg-muted rounded text-xs">Ctrl + K</kbd>
              </div>
            </div>
            <Button variant="outline" size="sm" onClick={() => setShowShortcuts(false)} className="w-full mt-4 cursor-pointer transition">
              Close
            </Button>
          </Card>
        </div>
      )}
    </div>
  )
}
