import axios from "axios";

const BASE_URL = "http://127.0.0.1:5000";

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