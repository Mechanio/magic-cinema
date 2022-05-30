import React, {useState} from 'react'
import {useNavigate} from "react-router-dom";
import fetchservice from "../services/fetch.service";

export default function CreateAuditorium() {
    const [seats, setSeats] = useState('');
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();

        try {
            const response = await fetchservice.createAuditorium(seats)
            if(response && response.data && response.data.id) {
                navigate("/auditoriums")
            } else {
                throw new Error(response.response.data.message)
            }
        } catch (err) {
            if(err.message === "Forbidden") {
                alert("Only admins can create auditorium")
            } else {
                alert(err)
            }
        }
    }

    return (
        <div className="createDirector">
            <h2 className="text-center">Add a New Auditorium</h2>
            <form onSubmit={handleSubmit}>
                <div className="text-center form-group">
                    <label className="form-label">Seats:</label>
                    <input className="w-25" type="text" required value={seats} onChange={(e) => setSeats(e.target.value)}/>
                </div>
                <div className="text-center">
                    <button className="btn btn-primary">Create</button>
                </div>
            </form>
        </div>
    )
}


