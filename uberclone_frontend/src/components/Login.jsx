import axios from 'axios';
import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import DriverLocationTracker from './DriverLocation'; // Import the component

const Login = () => {
    const navigate = useNavigate();
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const [validationErrors, setValidationErrors] = useState({});
    const [isLoggedIn, setIsLoggedIn] = useState(false); // State to track if user is logged in

    const validate = () => {
        const errors = {};
        if (!username.trim()) {
            errors.username = 'Username is required';
        } else if (username.length < 3) {
            errors.username = 'Username must be more than 3 characters.';
        } else if (username.length > 20) {
            errors.username = 'Username must be less than 20 characters.';
        }

        if (!password) {
            errors.password = 'Password is required';
        } else if (password.length < 6) {
            errors.password = 'Password must be at least 6 characters long';
        }
        return errors;
    };


    // handle the form submission
    const handleSubmit = async (e) => {
        e.preventDefault();
        const errors = validate();
        if (Object.keys(errors).length > 0) {
            setValidationErrors(errors);
            return;
        }

        try {
            const response = await axios.post('http://127.0.0.1:8000/login/', { username, password });
            const { access, refresh } = response.data.token;
            localStorage.setItem('accessToken', access);
            localStorage.setItem('refreshToken', refresh);
            localStorage.setItem('user', JSON.stringify(response.data.data));
            
            // setIsLoggedIn(true); // Set logged-in state to true
            
            navigate('/'); // Redirect to another page if needed
        } catch (error) {
            setError('Login failed. Please check your credentials and try again.');
        }
    };

    return (
        <div className="flex items-center justify-center min-h-screen bg-gray-100">
            <form onSubmit={handleSubmit} className="bg-white p-6 mt-5 mb-5 rounded-2xl shadow-md w-full max-w-md">
                <h2 className="text-2xl text-center font-bold mb-6">Login</h2>
                <div className="mb-4">
                    <label htmlFor="username" className="block text-gray-700 mb-2">Username:</label>
                    <input
                        type="text"
                        value={username}
                        onChange={(e) => {
                            setUsername(e.target.value);
                            setValidationErrors((prev) => ({ ...prev, username: '' }));
                        }}
                        required
                        className="w-full px-3 py-2 border rounded-lg focus:outline-none focus:border-blue-500"
                    />
                    {validationErrors.username && <p className="text-red-500 text-sm mt-1">{validationErrors.username}</p>}
                </div>

                <div className="mb-4">
                    <label htmlFor="password" className="block text-gray-700 mb-2">Password:</label>
                    <input
                        type="password"
                        value={password}
                        onChange={(e) => {
                            setPassword(e.target.value);
                            setValidationErrors((prev) => ({ ...prev, password: '' }));
                        }}
                        required
                        className="w-full px-3 py-2 border rounded-lg focus:outline-none focus:border-blue-500"
                    />
                    {validationErrors.password && <p className="text-red-500 text-sm mt-1">{validationErrors.password}</p>}
                </div>
                <button 
                    type="submit"
                    className="w-full bg-blue-500 text-white py-2 px-4 rounded-lg hover:bg-blue-600 focus:outline-none"
                >
                    Login
                </button>

                <p className='text-bold mt-3 -mb-2 text-center hover:text-gray-500'>
                    <Link to="/signup"> Create Account. Signup</Link>
                </p>
            </form>
            {error && <p style={{ color: 'red' }}>{error}</p>}
            {/* {isLoggedIn && <DriverLocationTracker />} Only show DriverLocationTracker if logged in */}
        </div>
    );
};

export default Login;
