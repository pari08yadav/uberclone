// import React, { useState } from "react";
// import { GoogleMap, LoadScript, Marker } from '@react-google-maps/api';
// import axios from 'axios';
// import { Link } from "react-router-dom";
// import { useNavigate } from "react-router-dom";
// import Logout from "./Logout";


// const Home = () => {
//     const [pickupLocation, setPickupLocation] = useState('');
//     const [dropLocation, setDropLocation] = useState('');
//     const [pickupCoordinates, setPickupCoordinates] = useState(null);
//     const [dropCoordinates, setDropCoordinates] = useState(null);
//     const [error, setError] = useState('');
//     const [success, setSuccess] = useState('');
//     const [menuOpen, setMenuOpen] = useState(false);


//     const mapContainerStyle = {
//         height: "400px",
//         width: "100%"
//     };

//     const center = {
//         lat: 28.7,
//         lng: 77.1
//     };

//     const navigate = useNavigate();
    
//     const handleRequestRide = async (e) => {
//         e.preventDefault();
//         const token = localStorage.getItem('accessToken');
//         if (!token) {
//             setError('You must be logged in to request a ride.');
//             return;
//         }

//         try {
//             const requestData = {
//                 pickup_location: pickupLocation,
//                 drop_location: dropLocation,
//             };
//             console.log("Request Data:", requestData);

//             const response = await axios.post(
//                 'http://127.0.0.1:8000/request_ride/',
//                 requestData,
//                 { headers: { Authorization: `Bearer ${token}` } }
//             );

//             setSuccess('Ride requested successfully!');
//             setError('');
//             console.log("Response Data:", response.data);
//             navigate(`/ride/${response.data.data.id}`);
//         } catch (error) {
//             setError('Failed to request ride. Please try again.');
//             setSuccess('');
//             console.error("Error:", error.response ? error.response.data : error.message);
//         }
//     };


//     return(
//         <div>
//             <header className="bg-gray-800 text-white p-4">
//                 <div className="container mx-auto flex justify-between items-center">
//                     <div className="text-xl flex ">
//                         <Link to="#" className=""><h1 className="text-2xl font-bold"> UberClone </h1></Link>
//                         <Link to="#" className="hover:text-gray-400 mx-5 mt-1">Trip</Link>
//                         <Link to="#" className="hover:text-gray-400 mt-1">Package</Link>
//                     </div>
//                     <nav className="space-x-4">
//                         <div className="flex items-center space-x-4">
//                             <Link to="#" className="hover:text-gray-400">My Trips</Link>
//                             <Link to="/" className="hover:text-gray-400"> Home </Link>
//                             <div className="relative">
//                                 <button 
//                                     onClick={() => setMenuOpen (!menuOpen)}
//                                     className="flex items-center  space-x-2 bg-white text-gray-800 rounded-full p-2 shadow-lg hover:bg-gray-200"
//                                 >
//                                     <span className="mx-2"> Username </span>
//                                     <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
//                                         <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 9l-7 7-7-7"></path>
//                                     </svg>
//                                 </button>
//                                 {menuOpen && (
//                                     <div className="absolute right-0 mt-2 w-48 bg-white text-black rounded shadow-lg z-50">
//                                         <ul>
//                                             <li>
//                                                 <Link to="/user/profile" className="block px-4 py-2 hover:bg-gray-200">Profile</Link>
//                                             </li>
//                                             <li>
//                                                 <Link to="/settings" className="block px-4 py-2 hover:bg-gray-200">Settings</Link>
//                                             </li>
//                                             <li>
//                                                 <button onClick={() => Logout()} className="block px-4 py-2 w-full text-left hover:bg-gray-200">Logout</button>
//                                             </li>
//                                         </ul>
//                                     </div>
//                                 )}
//                             </div>
//                         </div>
//                     </nav>
//                 </div>
//             </header>
//             <div className="flex">
//                 <div className="w-1/2 p-4">
//                     <h2 className="text-2xl font-bold mb-4">Request a Ride</h2>
//                     <div className="mb-4">
//                         <label className="block text-gray-700">Pickup Location</label>
//                         <input
//                             type="text"
//                             value={pickupLocation}
//                             onChange={(e) => setPickupLocation(e.target.value)}
//                             className="w-full p-2 border border-gray-300 rounded"
//                         />
//                     </div>
//                     <div className="mb-4">
//                         <label className="block text-gray-700">Drop Location</label>
//                         <input
//                             type="text"
//                             value={dropLocation}
//                             onChange={(e) => setDropLocation(e.target.value)}
//                             className="w-full p-2 border border-gray-300 rounded"
//                         />
//                     </div>
//                     <button
//                     onClick={handleRequestRide}
//                     className="bg-blue-500 text-white py-2 px-4 rounded hover:bg-violet-600 active:bg-violet-700 focus:outline-none focus:ring focus:ring-violet-300 "
//                     >
//                     Request Ride
//                     </button>
//                 </div>

//                 <div className="w-1/2 p-4">
//                     <LoadScript googleMapsApiKey="AIzaSyAaNCNlJiIE-fEPS3wY1JJGjHo57ucHC1U">
//                         <GoogleMap 
//                         mapContainerStyle={mapContainerStyle}
//                         center={ center }
//                         zoom={10}
//                         >
//                             {pickupCoordinates && <Marker position={pickupCoordinates} />}
//                             {dropCoordinates && <Marker position={dropCoordinates} />}
//                         </GoogleMap>
//                     </LoadScript>
//                 </div>
//             </div>
//         </div>
//     );
// }


// export default Home;