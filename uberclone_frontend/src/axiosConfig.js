import axios from 'axios';
import { useNavigate } from 'react-router-dom';

const setupAxiosInterceptors = (navigate) => {
    const onResponseError = (error) => {
        if (error.response && error.response.status === 401) {
            // Token expired or unauthorized
            localStorage.removeItem('accessToken');
            localStorage.removeItem('refreshToken');
            localStorage.removeItem('user');
            alert('Session expired. Please login again.');
            navigate('/login');
        }
        return Promise.reject(error);
    };

    axios.interceptors.response.use(
        response => response,
        error => onResponseError(error)
    );
};

export default setupAxiosInterceptors;
