import React, {useState} from 'react';
import axios from 'axios';
import {  useNavigate } from 'react-router-dom';


const Signup = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
    user_type: '', 
    phone_number: '',
  });

  const [errors, setErrors] = useState({});
  const [validationErrors, setValidationErrors] = useState({});


  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  }


  const validate = () => {
    const errors = {};
    if (!formData.username.trim()) {
      errors.username = 'Username is required';
    } else if (formData.username.length < 3) {
      errors.username = 'Username must be at least 3 characters long';
    } else if (formData.username.length > 20) {
      errors.username = 'Username must be 20 characters or less';
    }

    if (!formData.password) {
      errors.password = 'Password is required';
    } else if (formData.password.length < 6) {
      errors.password = 'Password must be at least 6 characters long';
    }

    if (!formData.email.trim()) {
      errors.email = 'Email is required';
    } else if (!/\S+@\S+\.\S+/.test(formData.email)) {
      errors.email = 'Email address is invalid';
    }

    if (!formData.email.trim()) {
      errors.email = 'Email is required';
    } else if (!/\S+@\S+\.\S+/.test(formData.email)) {
      errors.email = 'Email address is invalid';
    }

    if (!/^\d{10}$/.test(formData.phone_number)) {
      errors.phone_number = 'Phone number is invalid';
    }

    return errors;
  };


  const handleSubmit = async (e) => {
    e.preventDefault();
    const errors = validate();
    if (Object.keys(errors).length > 0) {
        setValidationErrors(errors);
        return;
    }
    console.log('Form submitted with data:', formData);
    
    try {
      const response = await axios.post('http://127.0.0.1:8000/signup/', formData, {
        headers: {
          'Content-Type': 'application/json'
        }
      });
      console.log(response.data)
      navigate('/login'); // Redirect to login page 
    } catch (error) {
      if (error.response && error.response.data){
        setErrors(error.response.data);
      }
    }
  };


  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-100">
      <form onSubmit={handleSubmit} className="bg-white p-6 mt-5 mb-5 rounded-2xl shadow-md w-full max-w-md">
        <h2 className="text-2xl text-center font-bold mb-6">Sign Up</h2>
        <div className="mb-4">
          <label htmlFor="username" className="block text-gray-700 mb-2">Username</label>
          <input 
          type="text" 
          name="username" 
          value={formData.username} 
          onChange={handleChange}
          className={`w-full px-2 py-2 border rounded-lg focus:outline-none ${validationErrors.username ? 'border-red-500' : 'focus:border-blue-500'}`}
          />
          {validationErrors.username && <p className="text-red-500 text-sm mt-1">{validationErrors.username}</p>}
        </div>

        <div className="mb-4">
          <label className="block text-gray-700 mb-2" htmlFor="email"> Email </label>
          <input 
          type="email" 
          name="email" 
          value={formData.email} 
          onChange={handleChange} 
          className={`w-full px-3 py-2 border rounded-lg focus:outline-none ${validationErrors.email ? 'border-red-500' : 'focus:border-blue-500'}`}
          />
          {validationErrors.email && <p className="text-red-500 text-sm mt-1">{validationErrors.email}</p>}
        </div>

        <div className='mb-4'> 
          <label className="block text-gray-700 mb-2" htmlFor="password">Password</label>
          <input 
          type="password" 
          name="password" 
          value={formData.password} 
          onChange={handleChange} 
          className={`w-full px-2 py-2 border rounded-lg focus:outline-none ${validationErrors.password ? 'border-red-500' : 'focus:border-blue-500'}`}
          />
          {validationErrors.password && <p className="text-red-500 text-sm mt-1">{validationErrors.password}</p>}
        </div>
        
        <div className='mb-4'>
          <label className="block text-gray-700 mb-2" htmlFor="user_type">User Type</label>
          <select 
          name="user_type" 
          value={formData.user_type} 
          onChange={handleChange}
          className={`w-full px-3 py-2 border rounded-lg focus:outline-none ${validationErrors.user_type ? 'border-red-500' : 'focus:border-blue-500'}`}
          >
            <option value="">Select Type</option>
            <option value="rider">Rider</option>
            <option value="driver">Driver</option>
          </select>

          {validationErrors.user_type && <p className="text-red-500 text-sm mt-1">{validationErrors.user_type}</p>}

        </div>
        
        <div className='mb-4'>
          <label className="block text-gray-700 mb-2" htmlFor="phone_number"> Phone Number </label>
          <input 
          type="text" 
          name="phone_number" 
          value={formData.phone_number} 
          onChange={handleChange} 
          className={`w-full px-3 py-2 border rounded-lg focus:outline-none ${validationErrors.phone_number ? 'border-red-500' : 'focus:border-blue-500'}`}
          />

          {/* {validationErrors.phone_number && <p className="text-red-500 text-sm mt-1">{validationErrors.phone_number}</p>} */}

        </div>
        <button 
        type="submit"
        className="w-full bg-blue-500 text-white py-2 px-4 rounded-lg hover:bg-blue-600 focus:outline-none"
        >
          Sign Up
        </button>
        {errors.non_field_errors && <p className="text-red-500 text-sm mt-1">{errors.non_field_errors}</p>}
      </form>
    </div>
  );
};

export default Signup;

