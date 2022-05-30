import React, {useState, useEffect} from 'react'
import fetchservice from "./services/fetch.service";
import axios from "axios";
import {Link} from "react-router-dom";

const Profile = () => {
    const [profileInfo, setProfileInfo] = useState("");
    const [password, setPassword] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault()
        try {
            await axios.patch("http://localhost:5000/api/users/" + profileInfo.id, {password})
                .then((response) => {
                    console.log(response.data.message)
                    if (response.data.message === "Updated") {
                        alert("Password changed")
                        // window.location.reload()
                    }
                },
                (error) => {
                console.log(error)
                })
        } catch (err) {
            console.log(err)
        }
    }

    const fetchData = async () => {
        await fetchservice.getProfileInfo()
            .then((response) => {
                setProfileInfo(response.data)
            })
    }

    useEffect(() => {
        fetchData()
    }, [])

    return (
        <div className="profile">
            {profileInfo && <>
                {/* TODO tickets*/}
                <h3>Firstname: {profileInfo.firstname}</h3>
                <h3>Lastname: {profileInfo.lastname}</h3>
                <h3>Email: {profileInfo.email}</h3>
                <div className="form-group row">
                    <label className="control-label col-sm-5">Tickets: </label>
                    <div className="col-sm-2">
                    {profileInfo.tickets.map(ticket => (
                            <div>
                                <Link to={`/sessions/${ticket.session_id}`}>
                                Ticket
                                </Link>
                            </div>
                            )
                        )}
                    </div>
                </div>
                <form onSubmit={handleSubmit}>
                    <label>Change password:  </label>
                    <input type="password" required value={password} onChange={(e) => setPassword(e.target.value)} />
                    <button className="btn btn-primary" type="submit">Change</button>
                </form>
                </>}
        </div>
    )
};

export default Profile