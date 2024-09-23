import React from "react";
import { Link } from "react-router-dom";
import { isAuthenticated } from "../utils/auth";
import Logout from "./Logout";

const Header = () => {
    const auth = isAuthenticated();

    return(
        <header className="bg-black text-white" >
            <div className="cantainer mx-10  flex justify-between items-center p-4">
                <div className="flex items-center space-x-6">
                    <Link to="/"><h1 className="text-2xl font-bold"> UberClone </h1></Link>
                    <nav className="flex space-x-4 mt-1">
                        <Link to="/ride" className="hover:text-gray-400">Ride</Link>
                        <Link to="/drive" className="hover:text-gray-400">Drive</Link>
                        <Link to="/" className="hover:text-gray-400">Business</Link>
                        <Link to="/" className="hover:text-gray-400">About</Link>
                    </nav>
                </div>
                <nav className="flex space-x-4">
                    {/* <Link to="/" className="hover:text-gray-400">Home</Link> */}
                    {!auth && <Link to="/login" className="hover:text-gray-400">Login</Link>}
                    {!auth && <Link to="/signup" className="hover:text-gray-400">Sign Up</Link>}
                    {auth && <button onClick={() => Logout()} className="hover:text-gray-400"> Logout </button>}
                </nav>
            </div>
        </header>
    );
};

export default Header;

