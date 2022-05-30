import React, {useState} from 'react'
import {useNavigate} from "react-router-dom";
import fetchservice from "../services/fetch.service";

export default function CreateSession() {
    const [movie, setMovie] = useState('')
    const [auditoriumId, setAuditoriumId] = useState('')
    const [sessionDate, setSessionDate] = useState('')
    const [sessionTime, setSessionTime] = useState('')
    const navigate = useNavigate()

    const handleSubmit = async (e) => {
        e.preventDefault()
        try {
            const dateArr = sessionDate.split('.')
            let day, month, year
            [day, month, year] = dateArr

            const timeArr = sessionTime.split(':')
            let hour, minute
            [hour, minute] = timeArr

            await fetchservice.getMovieInfoByName(movie.replace(' ', '%20'))
                .then((movieResp) => {
                    if (movieResp && movieResp.data && movieResp.data.id) {
                        return movieResp.data.id
                    } else {
                        throw new Error(movieResp)
                    }
                })
                .then(async (id) => {
                    await fetchservice.createSession(id, parseInt(auditoriumId), parseInt(year), parseInt(month), parseInt(day), parseInt(hour), parseInt(minute))
                        .then((response) => {
                            if (response && response.data && response.data.id) {
                            navigate("/sessions")
                        } else {
                            throw new Error(response)
                        }
                        })
                })
        } catch (err) {
            if (err.message === "Forbidden") {
                alert("Only admins can create session")
            } else {
                console.log(err)
                alert(err)
            }
        }
    }

    return (
        <div className="createSession">
            <h2 className="text-center">Add a New Session</h2>
            <form onSubmit={handleSubmit}>
                <div className="text-center form-group">
                    <label className="form-label">Name of movie: </label>
                    <input className="w-25" type="text" required value={movie}
                           onChange={(e) => setMovie(e.target.value)}/>
                </div>
                <div className="text-center">
                    <label className="form-label">Auditorium Id: </label>
                    <input className="w-25" type="text" required value={auditoriumId}
                           onChange={(e) => setAuditoriumId(e.target.value)}/>
                </div>
                <div className="text-center">
                    <label className="form-label">Session Date: </label>
                    <input className="w-25" type="text" required value={sessionDate} placeholder="dd.mm.yyyy"
                           onChange={(e) => setSessionDate(e.target.value)}/>
                </div>
                <div className="text-center">
                    <label className="form-label">Session Time: </label>
                    <input className="w-25" type="text" required value={sessionTime} placeholder="hh:mm"
                           onChange={(e) => setSessionTime(e.target.value)}/>
                </div>
                <div className="text-center">
                    <button className="btn btn-primary">Create</button>
                </div>
            </form>
        </div>
    )
}


