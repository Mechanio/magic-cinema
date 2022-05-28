import React, {useState, useEffect} from 'react'
import {Link, useNavigate, useParams} from 'react-router-dom';
import 'bootstrap/dist/css/bootstrap.css'
import fetchservice from "../services/fetch.service";


const Movie = () => {
    const [movie, setMovie] = useState()
    const {id} = useParams()
    const navigate = useNavigate()

    const updateMovie = async () => {
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
                        <label>
                            {movie?.name}
                        </label>
                    </div>
                </div>
                <div className="form-group row">
                    <label className="control-label col-sm-5">Description: </label>
                    <div className="col-sm-3">
                        <label>
                            {movie?.description}
                        </label>
                    </div>
                </div>
                <div className="form-group row">
                    <label className="control-label col-sm-5">Release date: </label>
                    <div className="col-sm-3">
                        <label>{movie?.release_date.split(" ").slice(0, -2).join(" ")}</label>
                    </div>
                </div>
                <div className="form-group row">
                    <label className="control-label col-sm-5">Director: </label>
                    <div className="col-sm-3">
                        <Link to={`/directors/${movie?.director.id}`}>
                            {movie?.director.firstname + ' ' + movie?.director.lastname}
                        </Link>
                    </div>
                </div>
                <div className="form-group row">
                    <label className="control-label col-sm-5">Genres: </label>
                    <div className="col-sm-3">
                        {movie?.genres.map(genre => (
                            <div>
                                <Link to={`/genres/${genre.id}`}>
                                {genre.genre}
                                </Link>
                            </div>
                            )
                        )}
                    </div>
                </div>
                <div className="form-group row">
                    <label className="control-label col-sm-5">Actors: </label>
                    <div className="col-sm-3">
                        {movie?.actors.map(actor => (
                            <div>
                                <Link to={`/actors/${actor.id}`}>
                                {actor.firstname + ' ' + actor.lastname}
                                </Link>
                            </div>
                            )
                        )}
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
                <Link to={`/movies/${movie?.id}/edit`}>
                    <input className="btn btn-primary" type="submit" value="Edit"/>
                </Link>
                <Link to={'/movies'}>
                    <input className="btn btn-danger" type={'button'} value="Back to list of movies"/>
                </Link>
            </form>
        </div>
    )
}

export default Movie






// import React, {useState, useEffect} from 'react'
// import {Link, useNavigate, useParams} from 'react-router-dom';
// import 'bootstrap/dist/css/bootstrap.css'
// import fetchservice from "../services/fetch.service";
//
//
// const Movie = () => {
//     const [movie, setMovie] = useState()
//     const {id} = useParams()
//     const navigate = useNavigate()
//
//     const updateMovie = async () => {
//         // try {
//         //     const response = await fetchservice.updateActor(id, actor?.firstname, actor?.lastname)
//         //     if (response && response.data && response.data.message === "Updated") {
//         //         navigate("/actors")
//         //
//         //     } else {
//         //         throw new Error(response.response.data.message)
//         //     }
//         // } catch (err) {
//         //     if (err.message === "Forbidden") {
//         //         alert("Only admins can update actor")
//         //     } else {
//         //         alert(err)
//         //     }
//         // }
//     }
//
//     useEffect(() => {
//         fetchservice.getMovieInfo(id)
//             .then((response) => {
//                     setMovie(response.data)
//                 }
//             )
//     }, [])
//
//     return (
//         <div className="movie">
//             <form className="form-horizontal">
//                 <div className="form-group row">
//                     <label className="control-label col-sm-5">Name:</label>
//                     <div className="col-sm-1">
//                         <input
//                             type={'text'}
//                             value={movie?.name}
//                             onChange={(event) =>
//                                 setMovie((prev) => ({...prev, name: event.target.value}))
//                             }
//                         />
//                     </div>
//                 </div>
//                 <div className="form-group row">
//                     <label className="control-label col-sm-5">Description: </label>
//                     <div className="col-sm-2">
//                         <textarea
//                                value={movie?.description}
//                                onChange={(event) =>
//                                    setMovie((prev) => ({...prev, description: event.target.value}))
//                         }
//                         />
//                     </div>
//                 </div>
//                 <div className="form-group row">
//                     <label className="control-label col-sm-5">Release date: </label>
//                     <div className="col-sm-2">
//                         <label>{movie?.release_date}</label>
//                     </div>
//                 </div>
//                 <div className="form-group row">
//                     <label className="control-label col-sm-5">Director: </label>
//                     <div className="col-sm-2">
//                         <Link to={`/directors/${movie?.director.id}`}>
//                             {movie?.director.firstname + ' ' + movie?.director.lastname}
//                         </Link>
//                     </div>
//                 </div>
//                 <div className="form-group row">
//                     <label className="control-label col-sm-5">Genres: </label>
//                     <div className="col-sm-2">
//                         {movie?.genres.map(genre => (
//                             <div>
//                                 <Link to={`/genres/${genre.id}`}>
//                                 {genre.genre}
//                                 </Link>
//                             </div>
//                             )
//                         )}
//                     </div>
//                 </div>
//                 <div className="form-group row">
//                     <label className="control-label col-sm-5">Actors: </label>
//                     <div className="col-sm-2">
//                         {movie?.actors.map(actor => (
//                             <div>
//                                 <Link to={`/actors/${actor.id}`}>
//                                 {actor.firstname + ' ' + actor.lastname}
//                                 </Link>
//                             </div>
//                             )
//                         )}
//                     </div>
//                 </div>
//                 <div className="form-group row">
//                     <label className="control-label col-sm-5">Sessions: </label>
//                     <div className="col-sm-2">
//                         {movie?.sessions.map(session => (
//                             <div>
//                                 <Link to={`/sessions/${session.id}`}>
//                                 {session.date}
//                                 </Link>
//                             </div>
//                             )
//                         )}
//                     </div>
//                 </div>
//                 <button className="btn btn-primary" type={'button'} onClick={updateMovie}>Update</button>
//                 <Link to={'/movies'}>
//                     <input className="btn btn-danger" type={'button'} value="Back to list of movies"/>
//                 </Link>
//             </form>
//         </div>
//     )
// }
//
// export default Movie