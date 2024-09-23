import React, { useEffect } from "react";
import { BrowserRouter as Router, Route, Routes, useNavigate } from "react-router-dom";
// import { Route, Routes } from "react-router-dom";
import SignupPage from "./pages/SignupPage";
import LoginPage from "./pages/LoginPage"
import LandingPage from "./pages/LandingPage";
import Layout from "./Loyout";
import RidePage from "./pages/RidePage";
import ProtectedRoute from './components/ProtectedRoute';
import DrivePage from "./pages/DrivePage";
import CreateDriverProfilePage from "./pages/CreateDriverProfilePage";
import UserProfilePage from "./pages/ProfilePage";
import RideDetails from "./pages/RideDetailsPage";
import setupAxiosInterceptors from "./axiosConfig";
import SecurityPage from "./pages/SecurityPage";
import ResetPasswordConfirmPage from "./pages/ResetRequestPasswordPage";


function App() {

  const navigate = useNavigate();

  useEffect(() => {
    setupAxiosInterceptors(navigate);
  }, [navigate]);
  
  return (
    <Routes>
        <Route path="/" element={<Layout/>} >
          <Route path='/login' element={<LoginPage/>} />
          <Route path='/signup' element={<SignupPage/>}/>
          <Route path='/' element={<LandingPage/>}/>
          <Route path="/drive" element={<DrivePage/>} />
          <Route path="/create_driver_profile" element={<CreateDriverProfilePage/>} />
          <Route path="/ride/:rideId" element={<RideDetails />} />
          <Route path="/reset_password/:token" element={<ResetPasswordConfirmPage/>} />
        </Route>
        
        <Route path="/" element={<ProtectedRoute />}>
            <Route path="/ride" element={<RidePage/>} />
            <Route path="/user/profile" element={<UserProfilePage />} />
            <Route path="/user/security" element={<SecurityPage />} />
        </Route>

        {/* <Route path='/ride' element={<RidePage/>}/> */}
    </Routes>
  );
}

export default App;
