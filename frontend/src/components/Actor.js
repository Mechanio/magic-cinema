import React, {useState, useEffect} from 'react'
import {Link, useNavigate, useParams} from 'react-router-dom';
import 'bootstrap/dist/css/bootstrap.css'
import fetchservice from "../services/fetch.service";


const Actor = () => {
    const [actor, setActor] = useState()
    const {id} = useParams()
    const navigate = useNavigate()

    const updateActor = async () => {
        try {
            const response = await fetchservice.updateActor(id, actor?.firstname, actor?.lastname)
            if (response && response.data && response.data.message === "Updated") {
                navigate("/actors")

            } else {
                throw new Error(response.response.data.message)
            }
        } catch (err) {
            if (err.message === "Forbidden") {
                alert("Only admins can update actor")
            } else {
                alert(err)
            }
        }
    }

    useEffect(() => {
        fetchservice.getActorInfo(id)
            .then((response) => {
                    setActor(response.data)
                }
            )
    }, [])

    return (
        <div className="actor">
            <form className="form-horizontal">
                <div className="form-group row">
                    <label className="control-label col-sm-5">Firstname:</label>
                    <div className="col-sm-2">
                        <input
                            type={'text'}
                            value={actor?.firstname}
                            onChange={(event) =>
                                setActor((prev) => ({...prev, firstname: event.target.value}))
                            }
                        />
                    </div>
                </div>
                <div className="form-group row">
                    <label className="control-label col-sm-5">Lastname: </label>
                    <div className="col-sm-2">
                        <input type={'text'}
                               value={actor?.lastname}
                               onChange={(event) =>
                                   setActor((prev) => ({...prev, lastname: event.target.value}))
                        }
                        />
                    </div>
                </div>
                <div className="form-group row">
                    <label className="control-label col-sm-5">Movies: </label>
                    <div className="col-sm-2">
                        {actor?.movies.map(movie => (
                            <div>
                                <Link to={`/movies/${movie.id}`}>
                                {movie.name}
                                </Link>
                            </div>
                            )
                        )}
                    </div>
                </div>
                <button className="btn btn-primary" type={'button'} onClick={updateActor}>Update</button>
                <Link to={'/actors'}>
                    <input className="btn btn-danger" type={'button'} value="Back to list of actors"/>
                </Link>
            </form>
        </div>
    )
}

export default Actor