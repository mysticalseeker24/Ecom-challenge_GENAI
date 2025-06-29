'use client'
import { useSelector } from "react-redux"
import { useDispatch } from "react-redux"
import { addMessage, clear } from "../../redux/features/chatSlice";
import InputBox from "@/components/InputBox";
import ChatMessagesBox from "@/components/ChatMessagesBox";
import { useEffect, useState } from "react";

export default function Home() {
  const dispatch = useDispatch();
  const [lengthOfMessages, setLengthOfMessages] = useState(0);
  const chat = useSelector(state => state.chat).value;
  useEffect(() => {
    setLengthOfMessages(chat?.messages?.length)
  }, [chat.messages])
  return <div className="h-screen w-screen bg-background flex flex-col justify-center items-center">
    {lengthOfMessages > 0 && <ChatMessagesBox messages={chat.messages} />}
  
    <InputBox lengthOfMessages={lengthOfMessages} />
    
  </div>
}
