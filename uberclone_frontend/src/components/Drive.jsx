import React from "react";
import axios from "axios";
import { Link, useNavigate } from "react-router-dom";
import drive_image1 from '../assets/landingImage/drive_image1.jpg';
import drive_image2 from '../assets/landingImage/drive_image2.png';
import { isAuthenticated } from "../utils/auth";


const Drive = () => {
    const auth = isAuthenticated();
    const navigate = useNavigate()

    const handleGetStarted = async () => {
        const token = localStorage.getItem('accessToken');
        try {
            const response = await axios.get('http://127.0.0.1:8000/check_driver_profile/', {
                headers: { Authorization: `Bearer ${token}` }
            });
            console.log("response", response.data)
            if (response.data.driver_profile){
                alert('Your driver account is already created.');
                navigate('/')
            }else {
                alert('You will be redirected to create your driver profile.');
                navigate('/create_driver_profile');
                
            }
        } catch (error) {
            if (error.response && error.response.status === 404) {
                alert('You will be redirected to create your driver profile.');
                navigate('/create_driver_profile');
            }else{
                console.error("Failed to check driver profile: ", error);
                alert('An error occurred while checking your driver profile. Please try again later.');
            }
        }
    } ;


    return (
        <div className="min-h-screen">

            {/* Navbar */}
            <div className="cantainer mx-10  flex justify-between items-center p-4">
                <div className="flex items-center space-x-6">
                    <Link to="/"><h1 className="text-2xl font-bold"> UberClone </h1></Link>
                    
                </div>
                <nav className="flex space-x-4 text-sm">
                    <Link to="#" className="hover:text-black text-gray-500 ">Overview</Link>
                    <Link to="#" className="hover:text-black text-gray-500">Requirements</Link>
                    <Link to="#" className="hover:text-black text-gray-500">Delivery Driver</Link>
                    <Link to="#" className="hover:text-black text-gray-500">Driving Basics</Link>
                    <Link to="#" className="hover:text-black text-gray-500">Earning</Link>
                    <Link to="#" className="hover:text-black text-gray-500">Safety</Link>
                    <Link to="#" className="hover:text-black text-gray-500">Uber Pro</Link>
                    <Link to="#" className="hover:text-black text-gray-500">Contact Us</Link>
                </nav>
            </div>

            {/* First section */}
            <div className="flex items-center justify-center p-8 bg-black">
                <div className="w-1/2 flex items-center justify-center p-8 text-white">
                    <div>
                        <h2 className="text-5xl font-bold mb-4">Driver when you want, make what you need</h2>
                        <p className="text-lg mb-4 mt-10">Earn on your own schedule.</p>
                        
                        <div className="mt-10"> 
                        {auth && <button onClick={handleGetStarted} className="bg-white text-black px-4 py-4 rounded-md hover:bg-blue-600 mr-4">Get Started</button>}
                        {/* {auth && <Link to="/create_driver_profile" className="bg-white text-black  px-4  py-4 rounded-md hover:bg-blue-600 mr-4">Get Started</Link>} */}
                        {!auth && <Link to="/login" className="mx-6 underline hover:bg-gray-800"> Already have an account? Sign in</Link>}
                        </div>
                    </div>
                </div>
                <div className="w-1/2 flex items-center justify-center p-8">
                    <img src={drive_image1} alt="Landing" className="max-h-fit rounded-lg shadow-lg"/> {/* Reduced height */}
                </div>
                
            </div>

            {/* Second Section */}
            <div className=" items-center justify-center  bg-white ">
                <div className="justify-center  ">
                    <h1 className="text-2xl font-bold p-8"> Why drive with us.</h1>
                    <img src={drive_image2} alt="Landing" className="h-80 rounded-lg shadow-lg"/>
                </div>
                <div className="flex bg-white p-8 pt-12 space-x-48 ">
                    <div className="justify-center items-center mx-10">
                        <p className=" font-semibold"> Set your own hours</p>
                        <h2>You decide when and how often you drive</h2>
                    </div>
                    <div>
                        <p className=" font-semibold"> Get paid fast</p>
                        <h2> Weekly payments in your bank account. </h2>
                    </div>
                    <div>
                        <p className=" font-semibold"> Get support at every turn. </p>
                        <h2> If there’s anything that you need, you can reach us anytime. </h2>
                    </div>
                    
                    
                </div>
            </div>
        </div>
    );
};


export default Drive;