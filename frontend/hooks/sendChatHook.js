import { useState } from "react";
import { useDispatch } from "react-redux";
import { addMessage } from "../redux/features/chatSlice"
const useSendChat = () => {

    const dispatch = useDispatch();
    const [loading, setLoading] = useState(false);
    const [data, setData] = useState();
    const CHAT_SERVICE_API = process.env.NEXT_PUBLIC_CHAT_SERVICE_API;

    const sendMessage = async (requestObject) => {
        try {

            setLoading(true);
            const response = await fetch(`${CHAT_SERVICE_API}/chat`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(requestObject)
            });
            if (response.status === 500) {
                alert("Something went wrong");
                let data = await response.json();
                throw new Error(data.response);
            }
            const data = await response.json();
            if (data?.requires_customer_id) {
                alert("Please provide your customer id");
            }
            if (data?.response) {
                dispatch(addMessage({ role: "assistant", message: data.response }))
            }
            setData(data?.response)

        } catch (error) {
            console.error("Error fetching fees:", error);
        } finally {
            setLoading(false);
        }
    };

    return { data, loading, sendMessage };
};

export default useSendChat;
