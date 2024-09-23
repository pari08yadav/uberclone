import React from "react";
import { faFacebookF, faTwitter, faInstagram, faLinkedinIn } from '@fortawesome/free-brands-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';



const Footer = () => {
    return (
        <footer className="bg-black text-white py-10">
            <div className="container mx-auto grid grid-cols-2 md:grid-cols-4 gap-8">
                <div>
                    <h3 className="text-xl font-semibold mb-6">Company</h3>
                    <ul className="space-y-3">
                        <li><a href="#" className="hover:text-gray-400">About Us</a></li>
                        <li><a href="#" className="hover:text-gray-400">Careers</a></li>
                        <li><a href="#" className="hover:text-gray-400">Press</a></li>
                        <li><a href="#" className="hover:text-gray-400">Blog</a></li>
                    </ul>
                </div>
                <div>
                    <h3 className="text-xl font-semibold mb-6">Product</h3>
                    <ul className="space-y-3">
                        <li><a href="#" className="hover:text-gray-400">Features</a></li>
                        <li><a href="#" className="hover:text-gray-400">Pricing</a></li>
                        <li><a href="#" className="hover:text-gray-400">Integrations</a></li>
                        <li><a href="#" className="hover:text-gray-400">API</a></li>
                    </ul>
                </div>
                <div>
                    <h3 className="text-xl font-semibold mb-4">Global Citizenship</h3>
                    <ul className="space-y-3">
                        <li><a href="#" className="hover:text-gray-400">Sustainability</a></li>
                        <li><a href="#" className="hover:text-gray-400">Diversity & Inclusion</a></li>
                        <li><a href="#" className="hover:text-gray-400">Community</a></li>
                        <li><a href="#" className="hover:text-gray-400">Ethics & Compliance</a></li>
                    </ul>
                </div>
                <div className="mx-10">
                    <h3 className="text-xl font-semibold mb-4 ">Travel</h3>
                    <ul className="space-y-3">
                        <li><a href="#" className="hover:text-gray-400">Business Travel</a></li>
                        <li><a href="#" className="hover:text-gray-400">Airports</a></li>
                        <li><a href="#" className="hover:text-gray-400">Cities</a></li>
                        <li><a href="#" className="hover:text-gray-400">Hotels</a></li>
                    </ul>
                </div>
            </div>
            <div className="container mx-auto text-center mt-16">
                <div className="flex justify-center space-x-10 mb-6">
                    <a href="#" className="hover:text-gray-400">
                        <FontAwesomeIcon icon={faFacebookF} size="2x" />
                    </a>
                    <a href="#" className="hover:text-gray-400">
                        <FontAwesomeIcon icon={faTwitter} size="2x" />
                    </a>
                    <a href="#" className="hover:text-gray-400">
                        <FontAwesomeIcon icon={faInstagram} size="2x" />
                    </a>
                    <a href="#" className="hover:text-gray-400">
                        <FontAwesomeIcon icon={faLinkedinIn} size="2x" />
                    </a>
                </div>
                
            </div>
            <div className="text-center mt-10">
                <p>&copy; {new Date().getFullYear()} UberClone. All rights reserved.</p>
            </div>
        </footer>
    );
};

export default Footer;