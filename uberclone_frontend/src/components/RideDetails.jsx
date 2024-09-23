import React, {useEffect, useState} from "react";
import axios from "axios";
import { useParams } from "react-router-dom";


const RideDetails = () => {
    const {rideId} = useParams();
    const [ride, setRide] = useState(null);
    const [error, setError] = useState('');

    useEffect(() => {
        const fetchRideDetails = async () => {
            try {
                const token = localStorage.getItem('accessToken');
                const response = await axios.get(`http://127.0.0.1:8000/ride_detail/${rideId}/`,{
                    headers: { Authorization: `Bearer ${token}` }
                });
                setRide(response.data.data);
            }catch (err) {
                setError('Failed to fetch ride request');
            }
        };

        fetchRideDetails();

    }, [rideId]);

    if (error) return <p>{error}</p>;
    if (!ride) return <p>Loading...</p>;

    return (
        <div className="p-4">
            <h2 className="text-2xl font-bold mb-4 text-center">Ride Details</h2>
            <div className="flex justify-between ">
                {/* Rider Details */}
                <div className="flex-1 mx-2 p-4 border rounded shadow-lg">
                    <h3 className="text-xl font-semibold mb-2">Rider</h3>
                    <p><strong>Username:</strong> {ride.rider.username}</p>
                    <p><strong>Email:</strong> {ride.rider.email}</p>
                    <p><strong>Phone Number:</strong> {ride.rider.phone_number}</p>
                    {/* Add more rider details if needed */}
                </div>

                {/* Ride Details */}
                <div className="flex-1 mx-2 p-4 border rounded shadow-lg">
                    <h3 className="text-xl font-semibold mb-2">Ride Information</h3>
                    <p><strong>Pickup Location:</strong> {ride.pickup_location}</p>
                    <p><strong>Drop Location:</strong> {ride.drop_location}</p>
                    <p><strong>Status:</strong> {ride.status}</p>
                    {/* Add more ride details if needed */}
                </div>

                {/* Driver Details */}
                <div className="flex-1 mx-2 p-4 border rounded shadow-lg">
                    <h3 className="text-xl font-semibold mb-2">Driver</h3>
                    <p><strong>Username:</strong> {ride.driver.username}</p>
                    <p><strong>Email:</strong> {ride.driver.email}</p>
                    <p><strong>Phone Number:</strong> {ride.driver.phone_number}</p>
                    {/* Add more driver details if needed */}
                </div>
            </div>
        </div>
    );


};

export default RideDetails;
