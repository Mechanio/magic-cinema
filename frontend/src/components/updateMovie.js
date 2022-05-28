import React, {useState, useEffect} from 'react'
import {Link, useNavigate, useParams} from 'react-router-dom';
import 'bootstrap/dist/css/bootstrap.css'
import fetchservice from "../services/fetch.service";


const UpdateMovie = () => {
    const [movie, setMovie] = useState()
    const [director, setDirector] = useState()
    const [genres, setGenres] = useState()
    const [actors, setActors] = useState()

    const {id} = useParams()
    const navigate = useNavigate()

    const updateMovie = async () => {
        try {
            let directorArr = movie.director.split(' ').where((s) => !s.isEmpty).toList()
            directorArr.map(s => s.trim())
            let directorFirstname, directorLastname
            [directorFirstname, directorLastname] = directorArr

            let genresArr = movie.genres.split(',').where((s) => !s.isEmpty).toList()
            genresArr.map(s => s.trim())

            let actorsArr = movie.actors.split(',').where((s) => !s.isEmpty).toList()
            actorsArr.map(s => s.trim())

            await fetchservice.getDirectorInfoByName(directorFirstname, directorLastname)
                .then((directorResp) => {
                    if (directorResp && directorResp.data && directorResp.data.id) {
                        return directorResp.data.id
                    } else {
                        throw new Error(directorResp)
                    }
                })
                .then(async (dir_id) => {
                    await fetchservice.updateMovie(id, movie.name, movie.description, dir_id, genresArr, actorsArr)
                        .then((response) => {
                            if (response && response.data && response.data.message === "Updated") {
                            navigate(`/movies/${id}`)
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

        // try {
        //     const response = await fetchservice.updateActor(id, actor?.firstname, actor?.lastname)
        //     if (response && response.data && response.data.message === "Updated") {
        //         navigate("/actors")
        //
        //     } else {
        //         throw new Error(response.response.data.message)
        //     }
        // } catch (err) {
        //     if (err.message === "Forbidden") {
        //         alert("Only admins can update actor")
        //     } else {
        //         alert(err)
        //     }
        // }
    }
    //
    //   const handleSubmit = async (e) => {
    //     e.preventDefault()

    //             .then(async (id) => {
    //                 await fetchservice.createMovie(name, description, id, year, month, day, genres.split(', '), actors.split(', '))
    //                     .then((response) => {
    //                         if (response && response.data && response.data.id) {
    //                         navigate("/movies")
    //                     } else {
    //                         throw new Error(response)
    //                     }
    //                     })
    //             })
    //     } catch (err) {
    //         if (err.message === "Forbidden") {
    //             alert("Only admins can create actor")
    //         } else {
    //             console.log(err)
    //             alert(err)
    //         }
    //     }
    // }

    useEffect(() => {
        fetchservice.getMovieInfo(id)
            .then((response) => {
                    setMovie(response.data)
                }
            )
    }, [])

    return (
        <div className="movie">
            <form className="form-horizontal">
                <div className="form-group row">
                    <label className="control-label col-sm-5">Name:</label>
                    <div className="col-sm-3">
                        <input
                            type={'text'}
                            value={movie?.name}
                            onChange={(event) =>
                                setMovie((prev) => ({...prev, name: event.target.value}))
                            }
                        />
                    </div>
                </div>
                <div className="form-group row">
                    <label className="control-label col-sm-5">Description: </label>
                    <div className="col-sm-3">
                        <textarea
                               value={movie?.description}
                               onChange={(event) =>
                                   setMovie((prev) => ({...prev, description: event.target.value}))
                        }
                        />
                    </div>
                </div>
                <div className="form-group row">
                    <label className="control-label col-sm-5">Release date: </label>
                    <div className="col-sm-3">
                        <label>{movie?.release_date}</label>
                    </div>
                </div>
                <div className="form-group row">
                    <label className="control-label col-sm-5">Director: </label>
                    <div className="col-sm-3">
                            <input
                            type={'text'}
                            value={movie?.director.firstname + ' ' + movie?.director.lastname}
                            onChange={(event) => setDirector(event.target.value)}
                        />
                    </div>
                </div>
                <div className="form-group row">
                    <label className="control-label col-sm-5">Genres: </label>
                    <div className="col-sm-3">
                            <div>
                                <input
                                type={'text'}
                                value={movie?.genres.map(genre => (genre.genre))}
                                onChange={(event) =>
                                    setMovie((prev) => ({...prev, genres: event.target.value}))
                                }/>
                            </div>
                    </div>
                </div>
                <div className="form-group row">
                    <label className="control-label col-sm-5">Actors: </label>
                    <div className="col-sm-3">
                        <div>
                            <input
                            type={'text'}
                            value={movie?.actors.map(actor => (actor.firstname + ' ' + actor.lastname))}
                            onChange={(event) =>
                                setMovie((prev) => ({...prev, actors: event.target.value}))
                            }/>
                        </div>
                    </div>
                </div>
                <div className="form-group row">
                    <label className="control-label col-sm-5">Sessions: </label>
                    <div className="col-sm-3">
                        {movie?.sessions.map(session => (
                            <div>
                                <Link to={`/sessions/${session.id}`}>
                                {session.date}
                                </Link>
                            </div>
                            )
                        )}
                    </div>
                </div>
                {/*<button className="btn btn-primary" type={'button'} onClick={updateMovie}>Update</button>*/}
                <Link to={'/movies'}>
                    <input className="btn btn-danger" type={'button'} value="Back to list of movies"/>
                </Link>
            </form>
        </div>
    )
}

export default UpdateMovie