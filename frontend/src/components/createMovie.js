import React, {useState} from 'react'
import {useNavigate} from "react-router-dom";
import fetchservice from "../services/fetch.service";

export default function CreateMovie() {
    const [name, setName] = useState('')
    const [description, setDescription] = useState('')
    const [releaseDate, setReleaseDate] = useState('')
    const [director, setDirector] = useState('')
    const [genres, setGenres] = useState('')
    const [actors, setActors] = useState('')
    const navigate = useNavigate()

    const handleSubmit = async (e) => {
        e.preventDefault()
        try {
            let directorArr = director.split(' ')
            let directorFirstname, directorLastname
            [directorFirstname, directorLastname] = directorArr

            const dateArr = releaseDate.split('.')
            let day, month, year;
            [day, month, year] = dateArr

            await fetchservice.getDirectorInfoByName(directorFirstname, directorLastname)
                .then((directorResp) => {
                    if (directorResp && directorResp.data && directorResp.data.id) {
                        return directorResp.data.id
                    } else {
                        throw new Error(directorResp)
                    }
                })
                .then(async (id) => {
                    await fetchservice.createMovie(name, description, id, year, month, day, genres.split(', '), actors.split(', '))
                        .then((response) => {
                            if (response && response.data && response.data.id) {
                            navigate("/movies")
                        } else {
                            throw new Error(response)
                        }
                        })
                })
        } catch (err) {
            if (err.message === "Forbidden") {
                alert("Only admins can create actor")
            } else {
                console.log(err)
                alert(err)
            }
        }
    }

    return (
        <div className="createActor">
            <h2 className="text-center">Add a New Actor</h2>
            <form onSubmit={handleSubmit}>
                <div className="text-center form-group">
                    <label className="form-label">Name: </label>
                    <input className="w-25" type="text" required value={name}
                           onChange={(e) => setName(e.target.value)}/>
                </div>
                <div className="text-center">
                    <label className="form-label">Description: </label>
                    <input className="w-25" type="text" required value={description}
                           onChange={(e) => setDescription(e.target.value)}/>
                </div>
                <div className="text-center">
                    <label className="form-label">Release Date: </label>
                    <input className="w-25" type="text" required value={releaseDate} placeholder="dd.mm.yyyy"
                           onChange={(e) => setReleaseDate(e.target.value)}/>
                </div>
                <div className="text-center">
                    <label className="form-label">Director: </label>
                    <input className="w-25" type="text" required value={director} placeholder="Name Surname"
                           onChange={(e) => setDirector(e.target.value)}/>
                </div>
                <div className="text-center">
                    <label className="form-label">Genres: </label>
                    <input className="w-25" type="text" required value={genres} placeholder="Genre name, genre name"
                           onChange={(e) => setGenres(e.target.value)}/>
                </div>
                <div className="text-center">
                    <label className="form-label">Actors: </label>
                    <input className="w-25" type="text" required value={actors} placeholder="Name Surname, Name Surname"
                           onChange={(e) => setActors(e.target.value)}/>
                </div>
                <div className="text-center">
                    <button className="btn btn-primary">Create</button>
                </div>
            </form>
        </div>
    )

}


