import React, { useEffect, useState, useRef } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

const RideRequest = () => {
    const navigate = useNavigate()
    const [map, setMap] = useState(null);
    const [pickupLocation, setPickupLocation] = useState("");
    const [dropLocation, setDropLocation] = useState("");
    const [pickupSuggestions, setPickupSuggestions] = useState([]);
    const [dropSuggestions, setDropSuggestions] = useState([]);
    const [pickupCoordinates, setPickupCoordinates] = useState(null);
    const [dropCoordinates, setDropCoordinates] = useState(null);
    const [message, setMessage] = useState("");
    const mapRef = useRef(null);


    useEffect(() => {
        if (window.MapmyIndia && window.MapmyIndia.Map) {
            const mapInstance = new window.MapmyIndia.Map('map', {
                center: [28.6139, 77.2090], // Default center, can be changed
                zoomControl: true,
                hybrid: true
            });
            setMap(mapInstance);
        } else {
            console.error('MapmyIndia SDK not loaded');
        }
    }, []);


    const handleAutocomplete = async (query, type) => {
        // setQuery(query);

        if (query.length > 2) {
            try {
                const token = localStorage.getItem('accessToken');
                if (!token) {
                    alert("Session is expired, login again.")
                    navigate('/login');
                }
                const response = await axios.get('http://127.0.0.1:8000/autocomplete_address/', {
                    params: { query: query },
                    headers: { Authorization: `Bearer ${token}` },
                });
            
                const suggestions = response.data.suggestedLocations;

                if (type === 'pickup') {
                    setPickupSuggestions(suggestions)
                }else {
                    setDropSuggestions(suggestions);
                }

            } catch (error) {
                console.error('Error fetching autocomplete suggestions:', error);
                }
        }
    };

    const handleGeocode = async (address, type) => {
        try {
            const token = localStorage.getItem("accessToken");
            if (!token) {
                alert("Session expired. Please log in again.");
                navigate("/login");
                return;
            }

            const response = await axios.get("http://127.0.0.1:8000/geocode_address/", {
                params: { address },
                headers: { Authorization: `Bearer ${token}` },
            });

            const { latitude, longitude } = response.data;
            
            if (type === "pickup") {
                setPickupCoordinates({ latitude, longitude });
                map.setView([latitude, longitude], 14);
                new window.L.marker([latitude, longitude])
                .addTo(map)
                .bindPopup('Pickup Location')
                .openPopup();
            } else {
                setDropCoordinates({ latitude, longitude });
                new window.L.marker([latitude, longitude])
                .addTo(map)
                .bindPopup('Drop Location')
                .openPopup();
            }

        }catch (error) {
            console.error('Error geocoding address:', error);
        }
    };


    // useEffect(() => {
    //     if (pickupCoordinates && dropCoordinates) {
    //         drawPolyline(pickupCoordinates, dropCoordinates);
    //     }
    // }, [pickupCoordinates, dropCoordinates]);


    const handleRequestRide = async () => {
        try {
            const token = localStorage.getItem("accessToken");
            if (!token) {
                alert("Session expired. Please log in again.");
                navigate("/login");
                return;
            }
            console.log(token)
            const requestData = {
                pickup_location: pickupLocation,
                drop_location: dropLocation,
                pickup_latitude: pickupCoordinates.latitude,
                pickup_longitude: pickupCoordinates.longitude,
                drop_latitude: dropCoordinates.latitude,
                drop_longitude: dropCoordinates.longitude,
            };

            console.log(requestData)
            
            const response = await axios.post(
                'http://127.0.0.1:8000/request_ride/',
                requestData,
                { headers: { Authorization: `Bearer ${token}` } }
            );

            // Check for specific message from the server
            if (response.data.message){
                setMessage(response.data.message);
            } else {
                setMessage("Ride requested successfully");
            }
            
            console.log("Ride requested successfully:", response.data);
        } catch (error) {
            setMessage("Error requesting ride. Please try again.");
            console.error("Error requesting ride:", error.response ? error.response.data : error.message);
        }
    };


    // const drawPolyline = async (pickupCoords, dropCoords) => {
    //     try {

    //         const token = localStorage.getItem("accessToken");
    //         if (!token) {
    //             alert("Session expired. Please log in again.");
    //             navigate("/login");
    //             return;
    //         }

    //         // Replace {api_key} with the actual API key variable
            
    //         // Request the route from MapmyIndia Routing API
    //         const map_access_token = import.meta.env.VITE_MAP_MY_INDIA_ACCESS_TOKEN;
    //         console.log(map_access_token)
    //         console.log("Pick latitude: " + pickupCoords.latitude, "pickup longitude: "+ pickupCoords.longitude, "drop latitude : " + dropCoords.latitude , "drop longitude: " + dropCoords.longitude)
            
    //         // const response = await axios.get(`https://apis.mapmyindia.com/advancedmaps/v1/${map_access_token}/route_adv/driving/${pickupCoords.latitude},${pickupCoords.longitude};${dropCoords.latitude},${dropCoords.longitude}`);
    //         const url = `https://apis.mapmyindia.com/advancedmaps/v1/4d62545a-ac9d-4174-ae87-4d5d5e5a8018/route_adv/driving/77.2090,28.6139;77.2311,28.6129`
            
    //         const response = await axios.get(url, {
    //             headers: {
    //                 'Content-Type': 'application/json',
    //             }
    //         })
            
    //         console.log(response.data)  

    //         const route = response.data.routes[0].geometry; //Assuming this is where the route geometry is returned

    //         // Decode the polyline (if it's encoded) and add it to the map
    //         const latlngs = window.L.Polyline.fromEncoded(route).getLatLngs(); // If the response is encoded

    //         if (map) {
    //             //Remove existing polylines
    //             map.eachLayer((layer) => {
    //                 if (layer instanceof window.L.Polyline) {
    //                     map.removeLayer(layer);
    //                 }
    //             });

    //             // Add the new polyline
    //             const polyline = window.L.polyline(latlngs, { color: 'blue' }).addTo(map);
    //             map.fitBounds(polyline.getBounds());
    //         }
    //     }catch(error) {
    //         console.error('Error drawing polyline:', error);
    //     }
    // };


    // const drawPolyline = (pickupCoords, dropCoords) => {
    //     const latlngs = [
    //         [pickupCoords.latitude, pickupCoords.longitude], // Fixing typo here
    //         [dropCoords.latitude, dropCoords.longitude],
    //     ];

    //     if (map) {
    //         // Remove existing polylines
    //         map.eachLayer((layer) => {
    //             if (layer instanceof window.L.Polyline) {
    //                 map.removeLayer(layer);
    //             }
    //         });

    //         // Add the new polyline
    //         const polyline = window.L.polyline(latlngs, { color: 'blue' }).addTo(map);
    //         map.fitBounds(polyline.getBounds());
    //     }
    // };


    const handleSuggestionClick = (suggestion, type) => {
        const address = suggestion.placeName;
        if (type === "pickup") {
            setPickupLocation(address);
            setPickupSuggestions([]);
            console.log(suggestion)
            handleGeocode(address, "pickup");
        } else {
            setDropLocation(address);
            setDropSuggestions([]);
            handleGeocode(address, "drop");
        }
    };
    

    return (
        <div className="flex h-screen">
            {/* Left side for user input */}
            <div className="w-1/3 p-8 bg-white ">
                <h2 className="text-2xl font-bold mb-4">Request a Ride</h2>
                <div className="mb-4">
                    <input
                        type="text"
                        value={pickupLocation}
                        onChange={(e) => {
                            setPickupLocation(e.target.value);
                            handleAutocomplete(e.target.value, "pickup");
                        }}
                        placeholder="Enter pickup location"
                        className="w-full p-2 border border-gray-300 rounded mb-2"
                    />
                    <ul className="border border-gray-300 rounded mb-2 bg-white">
                        {pickupSuggestions.map((suggestion, index) => (
                            <li
                                key={index}
                                onClick={() => handleSuggestionClick(suggestion, "pickup")}
                                className="p-2 cursor-pointer hover:bg-gray-200"
                            >
                                {suggestion.placeName}
                            </li>
                        ))}
                    </ul>
                </div>
                <div className="mb-4">
                    <input
                        type="text"
                        value={dropLocation}
                        onChange={(e) => {
                            setDropLocation(e.target.value);
                            handleAutocomplete(e.target.value, "drop");
                        }}
                        placeholder="Enter drop location"
                        className="w-full p-2 border border-gray-300 rounded mb-2"
                    />
                    <ul className="border border-gray-300 rounded mb-2 bg-white">
                        {dropSuggestions.map((suggestion, index) => (
                            <li
                                key={index}
                                onClick={() => handleSuggestionClick(suggestion, "drop")}
                                className="p-2 cursor-pointer hover:bg-gray-200"
                            >
                                {suggestion.placeName}
                            </li>
                        ))}
                    </ul>
                </div>
                <button
                    onClick={handleRequestRide}
                    disabled={!pickupCoordinates || !dropCoordinates}
                    className="w-full bg-green-500 text-white py-2 rounded hover:bg-green-600"
                >
                    Request Ride
                </button>
                {message && <p className="mt-4 text-center">{message}</p>}
            </div>

            {/* Right side for Map */}
            <div className="w-full p-5">
                <div id="map" className="w-full h-full border rounded px-5 py-5"></div>
            </div>
        </div>
    );
};

export default RideRequest;



