import React, {useState} from "react";
import axios from 'axios';
import { Link } from "react-router-dom";
import { useNavigate } from "react-router-dom";


const Security = () => {
    const [message, setMessage] = useState('');
    const [showResetButton, setShowResetButton] = useState(false);
    const navigate = useNavigate();


    const handleShowResetButton = () => {
        setShowResetButton(true);
    };


    const handlePasswordResetRequest = async (e) => {
        e.preventDefault();

        try {
            const token = localStorage.getItem('accessToken');
            if (!token) {
                setMessage('Session expired. Please log in again.');
                navigate('/login');
                return;
            }

            const response = await axios.post(
                'http://127.0.0.1:8000/password_reset/',
                {},
                {
                    headers: { Authorization: `Bearer ${token}` }
                }
            );

            setMessage(response.data.message || response.data.error);
        } catch (error) {
            if (error.response && error.response.status === 401) {
                setMessage('Session expired. Please log in again.');
                navigate('/login');
            } else {
                setMessage(error.response?.data.error || 'Failed to request password reset. Please try again.');
            }
        }
    };

    return (
        <div className="flex flex-col h-screen">
            {/* Header */}
            <header className="bg-black text-white py-4">
                <div className="container mx-auto flex justify-between items-center px-4">
                    <h1 className="text-2xl font-bold">User Account</h1>
                </div>
            </header>

            <div className="flex flex-1">
                {/* Sidebar */}
                <div className="w-1/4 bg-gray-100 p-4 border-r border-gray-300">
                    <h2 className="text-lg font-bold mb-4">Profile</h2>
                    <ul>
                        <li className="mb-2">
                            <Link to="/user/profile" className="hover:text-gray-400">Account info</Link>
                        </li>
                        <li className="mb-2">
                            <Link to="/user/security" className="hover:text-gray-400">Security</Link>
                        </li>
                        <li>
                            <Link to="/user/privacy" className="hover:text-gray-400">Privacy & Data</Link>
                        </li>
                    </ul>
                </div>

                {/* Main Components */}
                <div className="w-3/4 p-8">
                    <h1 className="font-bold text-4xl mb-6">Security</h1>

                    <div className="bg-white p-6 rounded shadow-md">
                        <h2 className="text-2xl font-bold mb-4">Reset Password</h2>
                        {!showResetButton ? (
                            <button
                                onClick={handleShowResetButton}
                                className="bg-blue-500 text-white py-2 px-4 rounded hover:bg-blue-600"
                            >
                                Update Password
                            </button>
                        ) : (
                            <form onSubmit={handlePasswordResetRequest}>
                                <button
                                    type="submit"
                                    className="bg-green-500 text-white py-2 px-4 rounded hover:bg-green-600"
                                >
                                    Send Password Reset Request
                                </button>
                            </form>
                        )}
                        {message && <p className={`mt-4 ${message.includes('Failed') || message.includes('not found') || message.includes('expired') ? 'text-red-500' : 'text-green-500'}`}>{message}</p>}
                    </div>
                </div>

            </div>
        </div>
    );

};

export default Security;



// import React, { useState } from "react";
// import axios from "axios";
// import { Link } from "react-router-dom";

// const Security = () => {
//     const [email, setEmail] = useState('');
//     const [message, setMessage] = useState('');
//     const [showResetForm, setShowResetForm] = useState(false);

//     const handlePasswordResetRequest = async (e) => {
//         e.preventDefault();

//         try {
//             const token = localStorage.getItem('accessToken');
//             const response = await axios.post(
//                 'http://127.0.0.1:8000/password_reset/',
//                 { email },
//                 {
//                     headers: { Authorization: `Bearer ${token}` }
//                 }
//             );
//             setMessage(response.data.message || response.data.error);
//         } catch (error) {
//             setMessage(error.response.data.error || 'Failed to request password reset. Please try again.');
//         }
//     };

//     return (
//         <div className="flex flex-col h-screen">
//             {/* Header */}
//             <header className="bg-black text-white py-4">
//                 <div className="container mx-auto flex justify-between items-center px-4">
//                     <h1 className="text-2xl font-bold">User Account</h1>
//                 </div>
//             </header>

//             <div className="flex flex-1">
//                 {/* Sidebar */}
//                 <div className="w-1/4 bg-gray-100 p-4 border-r border-gray-300">
//                     <h2 className="text-lg font-bold mb-4">Profile</h2>
//                     <ul>
//                         <li className="mb-2">
//                             <Link to="/user/profile" className="hover:text-gray-400">Account info</Link>
//                         </li>
//                         <li className="mb-2">
//                             <Link to="/user/security" className="hover:text-gray-400">Security</Link>
//                         </li>
//                         <li>
//                             <Link to="/user/privacy" className="hover:text-gray-400">Privacy & Data</Link>
//                         </li>
//                     </ul>
//                 </div>

//                 {/* Main content */}
//                 <div className="w-3/4 p-8">
//                     <h1 className="font-bold text-4xl mb-6">Security</h1>

//                     <div className="bg-white p-6 rounded shadow-md">
//                         <h2 className="text-2xl font-bold mb-4">Reset Password</h2>
//                         {!showResetForm && (
//                             <button
//                                 onClick={() => setShowResetForm(true)}
//                                 clas    sName="bg-blue-500 text-white py-2 px-4 rounded hover:bg-blue-600"
//                             >
//                                 Update Password
//                             </button>
//                         )}
//                         {showResetForm && (
//                             <form onSubmit={handlePasswordResetRequest}>
//                                 <div className="mb-4">
//                                     <label className="block text-gray-700">Email:</label>
//                                     <input
//                                         type="email"
//                                         value={email}
//                                         onChange={(e) => setEmail(e.target.value)}
//                                         className="w-full p-2 border border-gray-300 rounded"
//                                         required
//                                     />
//                                 </div>
//                                 {message && <p className={`mb-4 ${message.includes('Failed') || message.includes('not found') ? 'text-red-500' : 'text-green-500'}`}>{message}</p>}
//                                 <button type="submit" className="bg-blue-500 text-white py-2 px-4 rounded hover:bg-blue-600">
//                                     Send Password Reset Email
//                                 </button>
//                             </form>
//                         )}
//                     </div>
//                 </div>
//             </div>
//         </div>
//     );
// };

// export default Security;
