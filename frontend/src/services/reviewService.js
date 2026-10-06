import axios from "axios";

const BASE_URL = import.meta.env.VITE_API_URL;

export const reviewCode = async (code) => {
    const token = localStorage.getItem("token");

    const response = await axios.post(
        `${BASE_URL}/review`,
        {
            code: code
        },
        {
            headers: {
                Authorization: `Bearer ${token}`
            }
        }
    );

    return response.data;
};