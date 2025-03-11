import axios from "axios";

const API_BASE_URL = "http://127.0.0.1:8000"; 

export const getDetections = async () => {
    const response = await axios.get(`${API_BASE_URL}/detections`);
    return response.data;
};

export const getMessages = async () => {
    const response = await axios.get(`${API_BASE_URL}/telegram-messages`);
    return response.data;
};
