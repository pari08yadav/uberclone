import React from "react";

const Logout = () => {
    localStorage.removeItem('accessToken');
    window.location.reload();
}

export default Logout;
