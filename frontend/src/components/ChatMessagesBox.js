import React, { useEffect, useRef } from "react";
import { Bot, User } from "lucide-react";

export default function ChatMessagesBox({ messages = [] }) {

    const messagesEndRef = useRef(null)

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
    }
    useEffect(() => {
        scrollToBottom()
    }, [messages])

    return (
        <div className="p-4 max-w-3xl w-full mx-auto h-[85vh] mb-20 overflow-y-scroll pb-10 space-y-2">
            {messages.map((msg, index) => (
                <div
                    key={index}
                    className={`flex items-start space-x-2 ${msg.role === "user" ? "justify-end" : "justify-start"
                        }`}
                >
                    {msg.role === "assistant" && (
                        <Bot className="w-5 h-5 mt-1 text-gray-500" />
                    )}
                    <div
                        className={`rounded-2xl px-4 py-2 text-base whitespace-pre-wrap leading-6 max-w-[75%] ${msg.role === "user"
                            ? "bg-foreground text-white"
                            : "bg-foreground text-white"
                            }`}
                    >
                        {msg.message}
                    </div>
                    {msg.role === "user" && (
                        <User className="w-4 h-4 mt-1 text-blue-500" />
                    )}
                </div>
            ))}
            <div ref={messagesEndRef}></div>
        </div>
    );
};

