import React, { useState, useEffect} from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import { Link } from "react-router-dom";
import Logout from "./Logout";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faPen } from "@fortawesome/free-solid-svg-icons";


const UserProfile = () => {
    const [user, setUser] = useState(null);
    const navigate = useNavigate();
    const [editField, setEditField] = useState(null);
    const [updatedValue, setUpdatedValue] = useState('');
    const [menuOpen, setMenuOpen] = useState(false);
    const [profileImage, setProfileImage] = useState(null);
    const [message, setMessage] = useState('');


    useEffect(() => {
        const fetchUserProfile = async () => {
            const token = localStorage.getItem('accessToken');
            if (!token) {
                navigate('login');
                return;
            }

            try {
                const response = await axios.get('http://127.0.0.1:8000/user_details/', {
                    headers: { Authorization: `Bearer ${token}` }
                });
                setUser(response.data.data)
            }catch (error) {
                console.error('Failed to fetch user profile:', error);
                alert("Failed to fetch user profile")
                navigate('/login');
            }
        };

        fetchUserProfile();
    }, [navigate]);


    const handleImageUpload = async (e) => {
        const file = e.target.files[0];

        if (!file) {
            alert('Please select a file.');
            return;
        }

        const formData = new FormData();
        formData.append('profile_picture', file);

        try {
            const token = localStorage.getItem('accessToken');
            const response = await axios.patch(
                'http://127.0.0.1:8000/api/update_user_profile_picture/',
                formData,
                {
                    headers: {
                        Authorization: `Bearer ${token}`,
                        'Content-Type': 'multipart/form-data'
                    }
                }
            );

            setUser({ ...user, profile_picture_url: response.data.data.profile_picture_url});
            alert("Profile picture updated successfully");
        }catch (error) {
            alert("Error updating profile picture.")
            console.error("Failed to upload profile picture", error);
        }

    }

    const triggerFileInput = () => {
        document.getElementById('profilePictureInput').click();
    };
    
    
    // handle edit method
    // const handleEdit = (field) => {
    //     setEditField(field);
    //     setUpdatedValue(user[field]);
    // };

    // handle save method
    // const handleSave = async (field) => {
    //     const token = localStorage.getItem('accessToken');
    //     if (!token) {
    //         navigate('login');
    //         return;
    //     }

    //     try {
    //         const response = await axios.put(
    //             `http://127.0.0.1:8000/api/user_profile_update/`, // Update the endpoint as per your backend setup
    //             { [field]: updatedValue },
    //             { headers: { Authorization: `Bearer ${token}` } }
    //         );
    //         setUser({ ...user, [field]: updatedValue });
    //         setEditField(null);
    //     } catch (error) {
    //         console.error('Failed to update user profile:', error);
    //         alert("Failed to update user profile");
    //     }
    // };


    if (!user) 
        return <div> Loading... </div>



    return (
        <div className="flex flex-col h-screen">
            {/* Header */}
            <header className="bg-black text-white py-4">
                <div className="container mx-auto flex justify-between items-center px-4">
                    <h1 className="text-2xl font-bold">User Account</h1>
                    <nav className="space-x-4 flex">
                        
                        <div className="">
                                <button 
                                    onClick={() => setMenuOpen (!menuOpen)}
                                    className="flex items-center  space-x-2 bg-white text-gray-800 rounded-full p-2 shadow-lg hover:bg-gray-200"
                                >
                                    <span className="mx-2"> Username </span>
                                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 9l-7 7-7-7"></path>
                                    </svg>
                                </button>
                                {menuOpen && (
                                    <div className="absolute right-0 mt-2 w-48 bg-white text-black rounded shadow-lg z-50">
                                        <ul>
                                            <li>
                                                <Link to="/user/profile" className="block px-4 py-2 hover:bg-gray-200">Profile</Link>
                                            </li>
                                            <li>
                                                <Link to="/settings" className="block px-4 py-2 hover:bg-gray-200">Settings</Link>
                                            </li>
                                            <li>
                                                <button onClick={() => Logout()} className="block px-4 py-2 w-full text-left hover:bg-gray-200">Logout</button>
                                            </li>
                                            <li>
                                                <Link to="/" className="block px-4 py-2 hover:bg-gray-200">Home</Link>
                                            </li>
                                        </ul>
                                    </div>
                                )}
                            </div>
                    </nav>
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
                            <Link to="/" className="hover:text-gray-400">Privacy & Data</Link>
                        </li>
                    </ul>
                </div>

                {/* main content */}
                <div className="w-3/4 p-8">
                    <h1 className="font-bold text-4xl"> Accout Info </h1>

                    <div className="item-center mb-6 my-5">
                        {/* <div className="w-24 h-24 rounded-full bg-gray-300 mr-6"> */}
                            {/* Profile Logo */}
                            {/* <img src="profile_logo.png" alt="Profile" className="w-full h-full rounded-full object-cover" /> */}
                        {/* </div> */}

                        <div className="w-24 h-24 rounded-full bg-gray-300 mr-6 relative">
                            <img
                                src={user.profile_picture_url || "profile_logo.png"}
                                alt="Profile"
                                className="w-full h-full rounded-full object-cover"
                            />
                            <input
                                type="file"
                                accept="image/*"
                                id="profilePictureInput"
                                onChange={handleImageUpload}
                                className="absolute top-0 left-0 w-full h-full opacity-0 cursor-pointer"
                            />
                            <button
                                onClick={triggerFileInput}
                                className="absolute bottom-0 right-0  bg-gray-800 text-white rounded-full p-2 hover:bg-gray-700"
                                style={{ transform: 'translate(25%, 25%)' }}
                            >
                                <FontAwesomeIcon icon={faPen} />
                            </button>
                        </div>
                        

                        <div>
                            
                            <div className="bg-white rounded p-2 mt-3">
                                <h3 className="font-bold text-2xl">Basic Info</h3>
                                <div className="mb-4 my-3">
                                    <label className="block text-gray-900 font-semibold">Name:</label>
                                    <p className="text-gray-900">{user.username}</p>
                                </div>
                                
                                {/* <div className="mb-4 my-3">
                                    <label className="block text-gray-900 font-semibold">Name:</label>
                                    {editField === 'username' ? (
                                        <div className="flex">
                                            <input 
                                                type="text" 
                                                value={updatedValue} 
                                                onChange={(e) => setUpdatedValue(e.target.value)}
                                                className="w-full p-2 border border-gray-300 rounded"   
                                            />
                                            <button onClick={() => handleSave('username')} className="bg-blue-500 text-white py-1 px-2 rounded ml-2">
                                                Save
                                            </button>
                                        </div>
                                    ) : (
                                        <div className="flex justify-between items-center">
                                            <p className="text-gray-900">{user.username}</p>
                                            <button onClick={() => handleEdit('username')} className="text-blue-500">
                                                Edit
                                            </button>
                                        </div>
                                    )}
                                </div> */}

                                <hr className="mb-3" />
                                
                                <div className="mb-4">
                                    <label className="block text-gray-900 font-semibold">Phone Number:</label>
                                    <p className="text-gray-900"> +91{user.phone_number} </p>
                                </div>

                                {/* <div className="mb-4 my-3">
                                    <label className="block text-gray-900 font-semibold">Phone Number</label>
                                    {editField === 'phone_number' ? (
                                        <div className="flex">
                                            <input 
                                                type="text" 
                                                value={updatedValue} 
                                                onChange={(e) => setUpdatedValue(e.target.value)}
                                                className="w-full p-2 border border-gray-300 rounded"   
                                            />
                                            <button onClick={() => handleSave('phone_number')} className="bg-blue-500 text-white py-1 px-2 rounded ml-2">
                                                Save
                                            </button>
                                        </div>
                                    ) : (
                                        <div className="flex justify-between items-center">
                                            <p className="text-gray-900">{user.phone_number}</p>
                                            <button onClick={() => handleEdit('phone_number')} className="text-blue-500">
                                                Edit
                                            </button>
                                        </div>
                                    )}
                                </div> */}
                                
                                <hr className="mb-3" />
                                
                                <div className="mb-4">
                                    <label className="block text-gray-900 font-semibold">Email:</label>
                                    <p className="text-gray-700">{user.email}</p>
                                </div>
                                
                                {/* <div className="mb-4 my-3">
                                    <label className="block text-gray-900 font-semibold">Email:</label>
                                    {editField === 'email' ? (
                                        <div className="flex">
                                            <input 
                                                type="text" 
                                                value={updatedValue} 
                                                onChange={(e) => setUpdatedValue(e.target.value)}
                                                className="w-full p-2 border border-gray-300 rounded"   
                                            />
                                            <button onClick={() => handleSave('email')} className="bg-blue-500 text-white py-1 px-2 rounded ml-2">
                                                Save
                                            </button>
                                        </div>
                                    ) : (
                                        <div className="flex justify-between items-center">
                                            <p className="text-gray-900">{user.email}</p>
                                            <button onClick={() => handleEdit('email')} className="text-blue-500">
                                                Edit
                                            </button>
                                        </div>
                                    )}
                                </div> */}

                                <hr className="mb-3" />

                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );

};

export default UserProfile;