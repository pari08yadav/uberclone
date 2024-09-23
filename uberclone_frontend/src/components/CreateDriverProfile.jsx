import axios from "axios";
import React, { Profiler, useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";


const CreateDriverProfile = () => {
    const [formData, setFormData] = useState({
        license_number: '',
        vehicle_type: 'car',
        vehicle_registration_number: '',
        years_of_experience: '',
        profile_picture: null,
    });

    const [error, setError] = useState('');
    const [success, setSuccess] = useState('');
    const navigate = useNavigate();


    // useEffect(() => {
    //     const checkProfile = async () => {
    //         const token = localStorage.getItem('accessToken');
    //         if (!token) {
    //             navigate('/login');   // Navigate to landing Page
    //             return;
    //         }

    //         try { 
    //             const response = await axios.get('http://127.0.0.1:8000/check_driver_profile/', {
    //                 headers: {
    //                     Authorization: `Bearer ${token}`,
    //                 },
    //             });
    //             console.log(response.data.error)
    //             if (response.data.driver_profile) {
    //                 navigate('/') // Redirect to home if profile exists
    //             }
    //             handleSubmit()
    //         }catch (error) {
    //             if (error.response && error.response.status !== 404) {
    //                 setError('Failed to check driver profile. Please try again.')
    //             }
    //         }
    //     };

    //     checkProfile();
    // }, [navigate]);


    const handleChange = (e) => {
        const { name, value, files } = e.target;
        if (name === 'profile_picture'){
            setFormData({ ...formData, profile_picture: files[0] });
        }else {
            setFormData({ ...formData, [name]: value});
        }
    }; 


    // handling submit button
    const handleSubmit = async (e) => {
        e.preventDefault();
        const token = localStorage.getItem('accessToken')
        if (!token) {
            setError('You must be logged in to create a driver profile.');
            return;
        }

        const dataToSend = new FormData();
        dataToSend.append('license_number', formData.license_number);
        dataToSend.append('vehicle_type', formData.vehicle_type);
        dataToSend.append('vehicle_registration_number', formData.vehicle_registration_number);
        dataToSend.append('years_of_experience', formData.years_of_experience);
        if (formData.profile_picture) {
            dataToSend.append('profile_picture', formData.profile_picture);
        }

        try {
            const response = await axios.post(
                'http://127.0.0.1:8000/create_driver_profile/', dataToSend,
                {
                    headers: {
                        Authorization: `Bearer ${token}`,
                    },
                }
            );
            setSuccess('Driver profile created successfully!');
            setError('');
            console.log(response.data);
            navigate('/')
        } catch (error) {
            if (error.response) {
                console.log('Error response:', error.response.data)
                setError('Failed to create driver profile. Please try again. ' + error.response.data.error);
            }else if (error.request) {
                console.log('Error request:', error.request);
                setError('Failed to create driver profile. No response received.');
            }else {
                console.log('Error message:', error.message);
                setError('Failed to create driver profile. ' + error.message);
            }
            setSuccess('');
        }
    };


    return (
        <div className="flex items-center, justify-center min-h-screen bg-gray-100">
            <form onSubmit={handleSubmit} className="bg-white p-6 mt-5 mb-5 rounded-2xl shadow-md w-full max-w-md">
            <h2 className="text-2xl text-center font-bold mb-6">Create Driver Profile</h2>
            <div className="mb-4">
                    <label className="block text-gray-700 mb-2">License Number:</label>
                    <input
                        type="text"
                        name="license_number"
                        value={formData.license_number}
                        onChange={handleChange}
                        className="w-full px-3 py-2 border rounded-lg focus:outline-none focus:border-blue-500"
                        required
                    />
                </div>
                <div className="mb-4">
                    <label className="block text-gray-700 mb-2">Vehicle Type:</label>
                    <select
                        name="vehicle_type"
                        value={formData.vehicle_type}
                        onChange={handleChange}
                        className="w-full px-3 py-2 border rounded-lg focus:outline-none focus:border-blue-500"
                        required
                    >
                        <option value="car">Car</option>
                        <option value="auto">Auto</option>
                        <option value="bike">Bike</option>
                    </select>
                </div>
                <div className="mb-4">
                    <label className="block text-gray-700 mb-2">Vehicle Registration Number:</label>
                    <input
                        type="text"
                        name="vehicle_registration_number"
                        value={formData.vehicle_registration_number}
                        onChange={handleChange}
                        className="w-full px-3 py-2 border rounded-lg focus:outline-none focus:border-blue-500"
                        required
                    />
                </div>
                <div className="mb-4">
                    <label className="block text-gray-700 mb-2">Years of Experience:</label>
                    <input
                        type="number"
                        name="years_of_experience"
                        value={formData.years_of_experience}
                        onChange={handleChange}
                        className="w-full px-3 py-2 border rounded-lg focus:outline-none focus:border-blue-500"
                        required
                    />
                </div>
                
                <button
                    type="submit"
                    className="w-full bg-blue-500 text-white py-2 px-4 rounded-lg hover:bg-blue-600 focus:outline-none"
                >
                    Create Profile
                </button>
            </form>
            {error && <p className="text-red-500 mt-4">{error}</p>}
            {success && <p className="text-green-500 mt-4">{success}</p>}
        </div>
    );

};

export default CreateDriverProfile;