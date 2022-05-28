import React, {useState, useEffect} from 'react'
import {Link, useNavigate, useParams} from 'react-router-dom';
import 'bootstrap/dist/css/bootstrap.css'
import fetchservice from "../services/fetch.service";


const Genre = () => {
    const [genre, setGenre] = useState()
    const {id} = useParams()
    const navigate = useNavigate()

    const updateGenre = async () => {
        try {
            const response = await fetchservice.updateGenre(id, genre?.genre)
            if (response && response.data && response.data.message === "Updated") {
                navigate("/genres")

            } else {
                throw new Error(response.response.data.message)
            }
        } catch (err) {
            if (err.message === "Forbidden") {
                alert("Only admins can update genre")
            } else {
                alert(err)
            }
        }
    }

    useEffect(() => {
        fetchservice.getGenreInfo(id)
            .then((response) => {
                    setGenre(response.data)
                }
            )
    }, [])

    return (
        <div className="genre">
            <form className="form-horizontal">
                <div className="form-group row">
                    <label className="control-label col-sm-5">Genre name:</label>
                    <div className="col-sm-2">
                        <input
                            type={'text'}
                            value={genre?.genre}
                            onChange={(event) =>
                                setGenre((prev) => ({...prev, genre: event.target.value}))
                            }
                        />
                    </div>
                </div>
                <div className="form-group row">
                    <label className="control-label col-sm-5">Movies: </label>
                    <div className="col-sm-2">
                        {genre?.movies.map(movie => (
                            <div>
                                <Link to={`/movies/${movie.id}`}>
                                {movie.name}
                                </Link>
                            </div>
                            )
                        )}
                    </div>
                </div>
                <button className="btn btn-primary" type={'button'} onClick={updateGenre}>Update</button>
                <Link to={'/genres'}>
                    <input className="btn btn-danger" type={'button'} value="Back to list of genres"/>
                </Link>
            </form>
        </div>
    )
}

export default Genre