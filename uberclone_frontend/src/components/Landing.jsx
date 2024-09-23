import React, {useEffect, useState} from "react";
import { Link } from "react-router-dom";
import landingImage1 from '../assets/landingImage/landing_image1.jpg'; // Correct path to your image
import landingImage2 from '../assets/landingImage/landing_image2.jpg'; 
import landingImage3 from '../assets/landingImage/landing_image3.jpg';
import landingImage4 from '../assets/landingImage/landing_image4.jpg';
import { isAuthenticated } from "../utils/auth";
import DriverLocationTracker from "./DriverLocation";


const Landing = () => {
    const [isLoggedIn, setIsLoggedIn] = useState(false);

    // Check if user is logged in by verifying the token or user data in localStorage
    useEffect(() => {
        const accessToken = localStorage.getItem('accessToken');
        if (accessToken) {
            setIsLoggedIn(true);
        }
    }, []);


    const auth = isAuthenticated()
    return(
        <div className="min-h-screen text-white">
            {/* first section */}
            <div className="flex items-center justify-center p-8 bg-black">
                <div className="w-1/2 flex items-center justify-center p-8">
                    <div>
                        <h1 className="text-4xl font-bold mb-4">Welcome to UberClone</h1>
                        <p className="text-lg mb-8">Experience the best rides with our top-rated drivers. Sign up today and start your journey with us.</p>
                        <div>
                            {!auth && <Link to="/signup" className="bg-blue-500 text-white py-2 px-4 rounded hover:bg-blue-600 mr-4">Sign Up</Link>}
                            {!auth && <Link to="/login" className="bg-gray-500 text-white py-2 px-4 rounded hover:bg-gray-600">Login</Link>}
                            {/* {auth && <Link to="/ride" className="bg-gray-500 text-white py-2 px-4 rounded hover:bg-gray-600">Book Your First Ride</Link>} */}
                            {auth && <Link to="/ride" className="bg-blue-500 text-white py-2 px-4 rounded hover:bg-blue-600 mr-4">Book Your Ride</Link>}
                        </div>
                    </div>
                </div>
                <div className="w-1/2 flex items-center justify-center p-8 ">
                    <img src={landingImage1} alt="Landing" className="rounded-lg shadow-lg h-full"/>
                </div>
            </div>

            {/* second section */}
            <div className="flex items-center justify-center p-8 bg-white">
                <div className="w-1/2 flex items-center justify-center p-8">
                    <img src={landingImage2} alt="Landing" className="max-h-fit rounded-lg shadow-lg"/> {/* Reduced height */}
                </div>
                <div className="w-1/2 flex items-center justify-center p-8 text-black">
                    <div>
                        <h2 className="text-5xl font-bold mb-4">Driver when you want, make what you need</h2>
                        <p className="text-lg mb-4">Make money on your schedule with deliveries or rides--or both. You can use your own car or choose a rental through Uber.</p>
                        <ul className="list-disc list-inside">
                            <li className="mb-2">Reliable and Safe Rides</li>
                            <li className="mb-2">Affordable Pricing</li>
                            <li className="mb-2">24/7 Customer Support</li>
                            <li className="mb-2">Easy Booking Process</li>
                        </ul>
                        <div className="mt-10"> 
                        <Link to="/" className="bg-black text-white py-4 px-4 rounded-lg hover:bg-gray-600 ">Get Started</Link>
                        <Link to="/signup" className="mx-6 underline hover:bg-red-100"> Already have an account? Sign in</Link>
                        </div>
                    </div>
                </div>
            </div>

            {/* third section */}
            <div className="flex items-center justify-center p-8 bg-white">
                <div className="w-1/2 flex items-center justify-center p-8 text-black">
                    <div>
                        <h2 className="text-5xl font-bold mb-12">The Uber you know, reimagined for business</h2>
                        <p className="text-lg mb-4">Uber for business is a platform managing global rides and meals, and local deliveries, for companies of any size.</p>
                        
                        <div className="mt-10"> 
                        <Link to="/" className="bg-black text-white py-4 px-4 rounded-lg hover:bg-gray-600 ">Get Started</Link>
                        <Link to="#" className="mx-6 underline hover:bg-red-100"> Check out our solution </Link>
                        </div>
                    </div>
                </div>
                <div className="w-1/2 flex items-center justify-center p-8">
                    <img src={landingImage3} alt="Landing" className="max-h-fit rounded-lg shadow-lg"/> {/* Reduced height */}
                </div>
            </div>

            {/* forth section */}
            <div className="flex items-center justify-center p-8 bg-white">
            <div className="w-1/2 flex items-center justify-center p-8">
                    <img src={landingImage4} alt="Landing" className="max-h-fit rounded-lg shadow-lg"/> {/* Reduced height */}
                </div>
                <div className="w-1/2 flex items-center justify-center p-8 text-black">
                    <div>
                        <h2 className="text-5xl font-bold mb-12">Making money by rending your car</h2>
                        <p className="text-lg mb-4 -mt-5">Connect with thousands of drivers and earn more per week with Uber's free fleet management tools.</p>
                        
                        <div className="mt-10"> 
                        <Link to="/" className="bg-black text-white py-4 px-4 rounded-lg hover:bg-gray-600 ">Get Started</Link>
                        
                        </div>
                    </div>
                </div>
            </div>
            {isLoggedIn && <DriverLocationTracker />}
        </div>        
    ) 
}

export default Landing;