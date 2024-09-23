import React, { useState, useEffect } from "react";
import axios from 'axios';

const DriverLocationTracker = () => {
    const [location, setLocation] = useState({ latitude: null, longitude: null });

    useEffect(() => {
        // Check if the Geolocation API is available
        if (navigator.geolocation) {
            alert("Parishram yadav")
            const watchId = navigator.geolocation.watchPosition(
                (position) => {
                    const { latitude, longitude } = position.coords;
                    setLocation({ latitude, longitude });
                    // Send the updated location to the backend
                    console.log("latitude" +  latitude + "longitude" + longitude)
                    updateDriverLocation(latitude, longitude);
                },
                (error) => {
                    console.error('Error getting location:', error.message);
                    alert('Error getting location: ' + error.message);
                },
                { enableHighAccuracy: true }
            );

            return () => navigator.geolocation.clearWatch(watchId);
        } else {
            alert('Geolocation is not supported by this browser.');
            console.error('Geolocation is not supported by this browser.');
        }
    }, []);

    const updateDriverLocation = async (latitude, longitude) => {
        try {
            const token = localStorage.getItem('accessToken');
            if (!token) {
                alert("Session expired. Please log in again.");
                return;
            }

            console.log("before api hit......")
            console.log(latitude,   longitude)
            const response = await axios.post(
                'http://127.0.0.1:8000/update_driver_location/', 
                {"latitude": latitude, "longitude": longitude },
                { headers: { Authorization: `Bearer ${token}` } }
            );
            console.log('Location updated:', response.data);

        } catch (error) {
            console.error('Error updating location:', error);
        }
    };

    return (
        <div>
            <p>Tracking driver location...</p>
        </div>
    );
};

export default DriverLocationTracker;
