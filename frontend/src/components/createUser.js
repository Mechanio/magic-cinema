import React, {useState} from 'react'
import {useNavigate} from "react-router-dom";
import fetchservice from "../services/fetch.service";

export default function CreateUser() {
    const [firstname, setFirstname] = useState('');
    const [lastname, setLastname] = useState('')
    const [email, setEmail] = useState('')
    const [password, setPassword] = useState('')
    const [isAdmin, setIsAdmin] = useState(false)

    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();

        try {
            const response = await fetchservice.createUser(firstname, lastname, email, password, isAdmin)
            if(response && response.data && response.data.id) {
                navigate("/users")
            } else {
                throw new Error(response.response.data.message)
            }
        } catch (err) {
            if(err.message === "Forbidden") {
                alert("Only admins can create genre")
            } else {
                alert(err)
            }
        }
    }


    return (
        <div className="createGenre">
            <h2 className="text-center">Add a New User</h2>
            <form onSubmit={handleSubmit}>
                <div className="text-center form-group">
                    <label className="form-label">Firstname:</label>
                    <input className="w-25" type="text" required value={firstname} onChange={(e) => setFirstname(e.target.value)}/>
                </div>
                <div className="text-center form-group">
                    <label className="form-label">Lastname:</label>
                    <input className="w-25" type="text" required value={lastname} onChange={(e) => setLastname(e.target.value)}/>
                </div>
                <div className="text-center form-group">
                    <label className="form-label">Email:</label>
                    <input className="w-25" type="text" required value={email} onChange={(e) => setEmail(e.target.value)}/>
                </div>
                <div className="text-center form-group">
                    <label className="form-label">Password:</label>
                    <input className="w-25" type="password" required value={password} onChange={(e) => setPassword(e.target.value)}/>
                </div>
                <div className="text-center form-group">
                    <label className="form-label">Admin:</label>
                    <input className="w-25" type="checkbox" checked={isAdmin} onChange={(e) => setIsAdmin(e.target.checked)}/>
                </div>
                <div className="text-center">
                    <button className="btn btn-primary">Create</button>
                </div>
            </form>
        </div>
    )

}


