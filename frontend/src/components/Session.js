import React, {useState, useEffect} from 'react'
import {Link, useNavigate, useParams} from 'react-router-dom';
import 'bootstrap/dist/css/bootstrap.css'
import fetchservice from "../services/fetch.service";


const Session = () => {
    const [session, setSession] = useState()
    const {id} = useParams()
    const navigate = useNavigate()

    const updateSession = async () => {
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
    const buyTicket = async () => {
        try {
            const response = await fetchservice.buyTicket(session?.id)
            if (response && response.data && response.data.id) {
                window.location.reload()
            } else {
                throw new Error(response.data.message)
            }
        } catch (err) {
            alert(err)
        }
    }


    useEffect(() => {
        fetchservice.getSessionInfo(id)
            .then((response) => {
                    setSession(response.data)
                }
            )
    }, [])

    return (
        <div className="session">
            <form className="form-horizontal">
                <div className="form-group row">
                    <label className="control-label col-sm-5">Movie name:</label>
                    <div className="col-sm-3">
                        <label>
                            {session?.movie.name}
                        </label>
                    </div>
                </div>
                <div className="form-group row">
                    <label className="control-label col-sm-5">Date: </label>
                    <div className="col-sm-3">
                        <label>
                            {session?.date}
                        </label>
                    </div>
                </div>
                <div className="form-group row">
                    <label className="control-label col-sm-5">Remaining seats: </label>
                    <div className="col-sm-3">
                        <label>{session?.remain_seats}</label>
                    </div>
                </div>
                <div className="form-group row">
                    <label className="control-label col-sm-5">All seats: </label>
                    <div className="col-sm-3">
                        <label>{session?.auditorium.seats}</label>
                    </div>
                </div>
                {/*<Link to={`/sessions/${session?.id}/edit`}>*/}
                {/*    <input className="btn btn-primary" type="submit" value="Edit"/>*/}
                {/*</Link>*/}
                <button className="btn btn-primary" type={'button'} onClick={buyTicket}>Buy a ticket</button>
                <Link to={'/sessions'}>
                    <input className="btn btn-danger" type={'button'} value="Back to list of sessions"/>
                </Link>
            </form>
        </div>
    )
}

export default Session