import React, {useState} from 'react'
import {useNavigate} from "react-router-dom";
import fetchservice from "../services/fetch.service";

export default function CreateActor() {
    const [firstname, setFirstname] = useState('');
    const [lastname, setLastname] = useState('');
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();

        try {
            const response = await fetchservice.createActor(firstname, lastname)
            if(response && response.data && response.data.id) {
                navigate("/actors")

            } else {
                throw new Error(response.response.data.message)
            }
        } catch (err) {
            if(err.message === "Forbidden") {
                alert("Only admins can create actor")
            } else {
                alert(err)
            }
        }
    }


    return (
        <div className="createActor">
            <h2 className="text-center">Add a New Actor</h2>
            <form onSubmit={handleSubmit}>
                <div className="text-center form-group">
                    <label className="form-label">Firstname:</label>
                    <input className="w-25" type="text" required value={firstname} onChange={(e) => setFirstname(e.target.value)}/>
                </div>
                <div className="text-center">
                    <label className="form-label">Lastname: </label>
                    <input className="w-25" type="text" required value={lastname} onChange={(e) => setLastname(e.target.value)}/>
                </div>
                <div className="text-center">
                    <button className="btn btn-primary">Create</button>
                </div>
            </form>
        </div>
    )

}


