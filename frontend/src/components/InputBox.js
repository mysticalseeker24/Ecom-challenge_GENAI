'use client'
import { ArrowUp, LoaderCircle } from "lucide-react";
import { useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { addMessage, clear } from "../../redux/features/chatSlice";
import useSendChat from "../../hooks/sendChatHook";


export default function InputBox({ lengthOfMessages }) {

    const { data, loading, sendMessage } = useSendChat();
    const [text, setText] = useState("");
    const [customerId, setCustomerId] = useState("");
    const dispatch = useDispatch();
    const chat = useSelector(state => state.chat).value
    const handleFormSubmit = async (e) => {
        e.preventDefault();
        if (text.trim().length === 0) {
            return
        }

        dispatch(
            addMessage({
                role: "user",
                message: text.trim()
            })
        )
        setText("");
        await sendMessage({
            messages: [...chat.messages, { role: "user", message: text.trim() }],
            conversation_id: "optional-conversation-id",
            customer_id: customerId,
            metadata: {}
        })
    }

    return <form style={{
        position: lengthOfMessages > 0 && "fixed",
        transition: "0.5s linear",
        bottom: lengthOfMessages > 0 && "3.5rem",
        maxWidth: lengthOfMessages > 0 && "48rem",
        width: lengthOfMessages > 0 && "66.66667%"

    }} onSubmit={handleFormSubmit} className={` bg-foreground overflow-hidden px-3  py-3 w-1/3 min-w-[400px] flex justify-between items-center rounded-3xl`}>
        {lengthOfMessages > 0 &&
            <button
                type="button"
                onClick={() => {
                    if (confirm("Are you sure you want to clear the conversation?")) {
                        dispatch(clear());
                    }
                }}
                className="text-sm px-3 my-2 py-2 bg-black rounded-lg text-white"
            >Clear</button>
        }

        <input value={text} onChange={(e) => { setText(e.target.value) }} className="ml-5 bg-foreground h-10 outline-none flex-1 text-white" placeholder="Ask anything..." />
        <button disabled={loading} className="bg-white h-9 w-9 rounded-full flex justify-center hover:bg-gray-400 transition-colors items-center">
            {loading ?
                <LoaderCircle className="animate-spin" size={22} />
                :
                <ArrowUp className="" size={22} />
            }
        </button>
    </form>
}