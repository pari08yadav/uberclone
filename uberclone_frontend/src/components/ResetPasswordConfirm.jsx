import React, {useState} from "react";
import axios from "axios";
import { useParams, useNavigate } from "react-router-dom";


const ResetPasswordConfirm = () => {
    const { token } = useParams();
    const [newPassword, setNewPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');
    const [message, setMessage] = useState('');
    const navigate = useNavigate();


    const handlePasswordResetConfirm = async (e) => {
        e.preventDefault();

        if (newPassword !== confirmPassword) {
            setMessage('Passwords do not match.');
            return;
        }

        try {
            console.log(token)
            const response = await axios.post(
                `http://127.0.0.1:8000/password_reset_confirm/${token}/`,
                { new_password: newPassword }
            );
            console.log(response)
            setMessage(response.data.message || response.data.error);
            if (response.data.message) {
                // Redirect to login page after successful password reset
                setTimeout(() => {
                    navigate('/login');
                }, 3000);
            }
        } catch (error) {
            console.error(error);
            setMessage(error.response?.data.error || 'Failed to reset password. Please try again.');
        }
    };


    return (
        <div className="flex flex-col h-screen justify-center items-center">
            <div className="bg-white p-6 rounded shadow-md w-full max-w-md">
                <h2 className="text-2xl font-bold mb-4">Reset Password</h2>
                <form onSubmit={handlePasswordResetConfirm}>
                    <div className="mb-4">
                        <label className="block text-gray-700">New Password:</label>
                        <input
                            type="password"
                            value={newPassword}
                            onChange={(e) => setNewPassword(e.target.value)}
                            className="w-full p-2 border border-gray-300 rounded"
                            required
                        />
                    </div>
                    <div className="mb-4">
                        <label className="block text-gray-700">Confirm Password:</label>
                        <input
                            type="password"
                            value={confirmPassword}
                            onChange={(e) => setConfirmPassword(e.target.value)}
                            className="w-full p-2 border border-gray-300 rounded"
                            required
                        />
                    </div>
                    {message && <p className={`mb-4 ${message.includes('Failed') || message.includes('not match') ? 'text-red-500' : 'text-green-500'}`}>{message}</p>}
                    <button type="submit" className="bg-blue-500 text-white py-2 px-4 rounded hover:bg-blue-600">
                        Reset Password
                    </button>
                </form>
            </div>
        </div>
    );
};

export default ResetPasswordConfirm;




// import React, {useState} from "react";
// import axios from "axios";
// import { useParams, useNavigate } from "react-router-dom";


// const ResetPasswordConfirm = () => {
//     const [newPassword, setNewPassword] = useState('');
//     const [confirmPassword, setConfirmPassword] = useState('');
//     const [message, setMessage] = useState('');
//     const { token } = useParams();
//     const navigate = useNavigate();

//     const handlePasswordResetConfirm = async (e) =>{
//         e.preventDefault();
//         if (newPassword !== confirmPassword) {
//             setMessage("Passwords do not match.");
//             return;
//         }
//         console.log(token)
//         try {
//             console.log(newPassword + " " + confirmPassword)
//             const response = await axios.post(
//                 `http://127.0.0.1:8000/password_reset_confirm/${token}/`,
//                 { new_password: newPassword }
//             );
//             console.log(response)
//             setMessage(response.data.message);
//             setTimeout(() => navigate('/login'), 3000); // Redirect to login after 3 seconds
//         }catch (error) {
//             console.log(error)
//             // console.log(error.response.data.error)
//             // console.log(response.data.error)
//         }
//     };   


//     return (
//         <div className="flex flex-col h-screen justify-center items-center">
//             <div className="w-full max-w-md p-8 space-y-3 rounded-xl bg-white shadow-lg">
//                 <h1 className="text-2xl font-bold text-center">Reset Password</h1>
//                 <form onSubmit={handlePasswordResetConfirm}>
//                     <div className="mb-4">
//                         <label className="block text-gray-700">New Password:</label>
//                         <input 
//                             type="password" 
//                             value={newPassword}
//                             onChange={(e) => setNewPassword(e.target.value)}
//                             className="w-full p-2 border border-gray-300 rounded"
//                             required
//                         />
//                     </div>
//                     <div className="mb-4">
//                         <label className="block text-gray-700">Confirm Password:</label>
//                         <input 
//                             type="password"
//                             value={confirmPassword}
//                             onChange={(e) => setConfirmPassword(e.target.value)}
//                             className="w-full p-2 border border-gray-300 rounded"
//                             required
                            
//                         />
//                     </div>
//                     <button type="submit" className="bg-blue-500 text-white py-2 px-4 rounded hover:bg-blue-600">
//                         Reset Password
//                     </button>
//                 </form>
//             </div>
//         </div>
//     );


// };

// export default ResetPasswordConfirm;

