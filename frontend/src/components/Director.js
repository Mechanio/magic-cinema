import React, {useState, useEffect} from 'react'
import {Link, useNavigate, useParams} from 'react-router-dom';
import 'bootstrap/dist/css/bootstrap.css'
import fetchservice from "../services/fetch.service";


const Director = () => {
    const [director, setDirector] = useState()
    const {id} = useParams()
    const navigate = useNavigate()

    const updateDirector = async () => {
        try {
            const response = await fetchservice.updateDirector(id, director?.firstname, director?.lastname)
            if (response && response.data && response.data.message === "Updated") {
                navigate("/directors")

            } else {
                throw new Error(response.response.data.message)
            }
        } catch (err) {
            if (err.message === "Forbidden") {
                alert("Only admins can update director")
            } else {
                alert(err)
            }
        }
    }

    useEffect(() => {
        fetchservice.getDirectorInfo(id)
            .then((response) => {
                    setDirector(response.data)
                }
            )
    }, [])

    return (
        <div className="director">
            <form className="form-horizontal">
                <div className="form-group row">
                    <label className="control-label col-sm-5">Firstname:</label>
                    <div className="col-sm-2">
                        <input
                            type={'text'}
                            value={director?.firstname}
                            onChange={(event) =>
                                setDirector((prev) => ({...prev, firstname: event.target.value}))
                            }
                        />
                    </div>
                </div>
                <div className="form-group row">
                    <label className="control-label col-sm-5">Lastname: </label>
                    <div className="col-sm-2">
                        <input type={'text'}
                               value={director?.lastname}
                               onChange={(event) =>
                                   setDirector((prev) => ({...prev, lastname: event.target.value}))
                        }
                        />
                    </div>
                </div>
                <div className="form-group row">
                    <label className="control-label col-sm-5">Movies: </label>
                    <div className="col-sm-2">
                        {director?.movies.map(movie => (
                            <div>
                                <Link to={`/movies/${movie.id}`}>
                                {movie.name}
                                </Link>
                            </div>
                            )
                        )}
                    </div>
                </div>
                <button className="btn btn-primary" type={'button'} onClick={updateDirector}>Update</button>
                <Link to={'/directors'}>
                    <input className="btn btn-danger" type={'button'} value="Back to list of directors"/>
                </Link>
            </form>
        </div>
    )
}

export default Director