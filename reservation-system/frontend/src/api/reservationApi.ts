import axios from 'axios';

const apiClient = axios.create({
    baseURL: 'http://localhost:8000', // バックエンドのURL
    headers: {
        'Content-Type': 'application/json',
    },
});

export const createReservation = async (reservationData) => {
    return await apiClient.post('/reservations', reservationData);
};
