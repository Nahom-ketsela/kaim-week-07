import React, { useEffect, useState } from "react";
import { getMessages } from "../api";

const MessagesTable = () => {
    const [messages, setMessages] = useState([]);

    useEffect(() => {
        getMessages().then(setMessages);
    }, []);

    return (
        <div>
            <h2>Telegram Messages</h2>
            <table>
                <thead>
                    <tr>
                        <th>ID</th><th>Channel</th><th>Message</th><th>Date</th>
                    </tr>
                </thead>
                <tbody>
                    {messages.map((message) => (
                        <tr key={message.id}>
                            <td>{message.id}</td>
                            <td>{message.channel_username}</td>
                            <td>{message.message}</td>
                            <td>{new Date(message.message_date).toLocaleString()}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
};

export default MessagesTable;
