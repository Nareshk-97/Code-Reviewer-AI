import axios from "axios";

const BASE_URL = "https://code-reviewer-ai-1-22gz.onrender.com";

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