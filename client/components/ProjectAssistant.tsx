"use client"

import type React from "react"

import { useState, useRef, useEffect } from "react"
import { Button } from "./ui/button"
import { Input } from "./ui/input"
import { Card, CardHeader, CardTitle } from "./ui/card"
import { ScrollArea } from "./ui/scroll-area"
import { Send, MessageCircle } from "lucide-react"

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
  const scrollAreaRef = useRef<HTMLDivElement>(null)
  const bottomRef = useRef<HTMLDivElement | null>(null)

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
  }

  return (
    <div className="w-full max-w-4xl mx-auto h-full max-h-[calc(100vh-160px)]">
      <Card className="h-full flex flex-col rounded-3xl border border-white/10 bg-white/70 backdrop-blur md:bg-white/60 dark:bg-zinc-900/60 shadow-[0_10px_40px_-15px_rgba(0,0,0,0.5)]">
        {/* Header */}
        <CardHeader className="border-b border-white/10 flex-shrink-0 py-4 bg-transparent">
          <CardTitle className="flex items-center gap-2 text-lg">
            <span className="inline-flex h-7 w-7 items-center justify-center rounded-md bg-emerald-500 text-black">
              <MessageCircle className="h-4 w-4" />
            </span>
            <span className="text-foreground">Project Assistant</span>
          </CardTitle>
        </CardHeader>

        {/* Messages Area */}
        <div className="flex flex-col">
          <ScrollArea ref={scrollAreaRef} className="bg-transparent h-96 md:h-[28rem]">
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
                    Thinking...
                  </div>
                </div>
              )}

              <div ref={bottomRef} className="h-px" />
            </div>
          </ScrollArea>

          {/* Input Area */}
          <div className="border-t border-white/10 bg-transparent flex-shrink-0">
            <div className="p-4">
              <div className="flex gap-3">
                <Input
                  value={currentMessage}
                  onChange={(e) => setCurrentMessage(e.target.value)}
                  onKeyDown={handleKeyDown}
                  placeholder="Type your prompt here..."
                  disabled={loading}
                  className="flex-1 h-11 rounded-xl bg-white/70 dark:bg-zinc-900/60 border-white/20 placeholder:text-muted-foreground"
                />
                <Button
                  onClick={handleSubmit}
                  disabled={loading || !currentMessage.trim()}
                  className="h-11 px-4 rounded-xl bg-emerald-500 hover:bg-emerald-400 text-black"
                >
                  <Send className="h-4 w-4" />
                </Button>
              </div>
            </div>
          </div>
        </div>
      </Card>
    </div>
  )
}
