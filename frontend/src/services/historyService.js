import axios from "axios";


const BASE_URL = "http://127.0.0.1:5000";


// ==========================================
// GET AUTH HEADERS
// ==========================================

const getAuthHeaders = () => {

    const token = localStorage.getItem("token");

    return {
        Authorization: `Bearer ${token}`
    };

};


// ==========================================
// GET REVIEW HISTORY
// ==========================================

export const getHistory = async () => {

    const response = await axios.get(
        `${BASE_URL}/history`,
        {
            headers: getAuthHeaders()
        }
    );

    return response.data;

};


// ==========================================
// SAVE REVIEW HISTORY
// ==========================================

export const saveHistory = async (
    language,
    code,
    review,
    score
) => {

    const response = await axios.post(
        `${BASE_URL}/history`,
        {
            language: language,
            code: code,
            review: review,
            score: score
        },
        {
            headers: getAuthHeaders()
        }
    );

    return response.data;

};


// ==========================================
// DELETE ONE REVIEW
// ==========================================

export const deleteHistory = async (id) => {

    const response = await axios.delete(
        `${BASE_URL}/history/${id}`,
        {
            headers: getAuthHeaders()
        }
    );

    return response.data;

};


// ==========================================
// CLEAR ALL HISTORY
// ==========================================

export const clearHistory = async () => {

    const response = await axios.delete(
        `${BASE_URL}/history`,
        {
            headers: getAuthHeaders()
        }
    );

    return response.data;

};