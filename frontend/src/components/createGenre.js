import React, {useState} from 'react'
import {useNavigate} from "react-router-dom";
import fetchservice from "../services/fetch.service";

export default function CreateGenre() {
    const [genre, setGenre] = useState('');
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();

        try {
            const response = await fetchservice.createGenre(genre)
            if(response && response.data && response.data.id) {
                navigate("/genres")

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
            <h2 className="text-center">Add a New Genre</h2>
            <form onSubmit={handleSubmit}>
                <div className="text-center form-group">
                    <label className="form-label">Genre name:</label>
                    <input className="w-25" type="text" required value={genre} onChange={(e) => setGenre(e.target.value)}/>
                </div>
                <div className="text-center">
                    <button className="btn btn-primary">Create</button>
                </div>
            </form>
        </div>
    )

}


