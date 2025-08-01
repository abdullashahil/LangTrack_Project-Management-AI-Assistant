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

  const scrollToBottom = () => {
    if (scrollAreaRef.current) {
      const scrollContainer = scrollAreaRef.current.querySelector("[data-radix-scroll-area-viewport]")
      if (scrollContainer) {
        scrollContainer.scrollTop = scrollContainer.scrollHeight
      }
    }
  }

  const renderMarkdown = (text: string) => {
    return text.split("\n").map((line, i) => {
      // Handle bullet points
      if (line.trim().startsWith("* ")) {
        const content = line.replace(/^\s*\*\s*/, "")
        return (
          <div key={i} className="flex items-start gap-2 my-1">
            <span className="text-gray-600 mt-1">•</span>
            <span dangerouslySetInnerHTML={{ __html: formatBoldText(content) }} />
          </div>
        )
      }

      // Handle regular lines with potential bold text
      if (line.trim()) {
        return <p key={i} className="my-1" dangerouslySetInnerHTML={{ __html: formatBoldText(line) }} />
      }

      // Empty lines
      return <br key={i} />
    })
  }

  const formatBoldText = (text: string) => {
    // Replace **text** with <strong>text</strong>
    return text.replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>")
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

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
        headers: {
          "Content-Type": "application/json",
        },
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
    } catch (error) {
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

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault()
      handleSubmit()
    }
  }

  return (
    <div className="w-full max-w-4xl mx-auto h-full max-h-[calc(100vh-120px)]">
      <Card className="h-full flex flex-col shadow-lg">
        {/* Header */}
        <CardHeader className="border-b flex-shrink-0 py-4">
          <CardTitle className="flex items-center gap-2 text-lg">
            <MessageCircle className="h-5 w-5" />
            Project Assistant
          </CardTitle>
        </CardHeader>

        {/* Messages Area */}
        <div className="flex-1 min-h-0 flex flex-col">
          <ScrollArea ref={scrollAreaRef} className="flex-1 bg-white h-1">
            <div className="p-4 space-y-4">
              {messages.map((message) => (
                <div key={message.id} className={`flex ${message.type === "user" ? "justify-end" : "justify-start"}`}>
                  <div
                    className={`max-w-[85%] rounded-lg px-4 py-3 ${
                      message.type === "user" ? "bg-blue-600 text-white" : "bg-gray-100 text-gray-900"
                    }`}
                  >
                    {message.type === "assistant" ? (
                      <div className="text-sm space-y-1">{renderMarkdown(message.content)}</div>
                    ) : (
                      <p className="text-sm">{message.content}</p>
                    )}
                  </div>
                </div>
              ))}

              {loading && (
                <div className="flex justify-start">
                  <div className="bg-gray-100 rounded-lg px-4 py-3">
                    <p className="text-sm text-gray-500">Thinking...</p>
                  </div>
                </div>
              )}
            </div>
          </ScrollArea>

          {/* Input Area */}
          <div className="border-t bg-white flex-shrink-0">
            <div className="p-4">
              <div className="flex gap-3">
                <Input
                  value={currentMessage}
                  onChange={(e) => setCurrentMessage(e.target.value)}
                  onKeyPress={handleKeyPress}
                  placeholder="Ask about your projects..."
                  disabled={loading}
                  className="flex-1 h-11"
                />
                <Button onClick={handleSubmit} disabled={loading || !currentMessage.trim()} className="h-11 px-4">
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
