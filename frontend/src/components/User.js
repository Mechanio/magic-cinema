import React, {useState, useEffect} from 'react'
import {Link, useNavigate, useParams} from 'react-router-dom';
import 'bootstrap/dist/css/bootstrap.css'
import fetchservice from "../services/fetch.service";


const User = () => {
    const [user, setUser] = useState()
    const {id} = useParams()
    const navigate = useNavigate()

    const updateUser = async () => {
        try {
            const response = await fetchservice.updateUser(id, user?.firstname, user?.lastname, user?.email)
            if (response && response.data && response.data.message === "Updated") {
                navigate("/users")

            } else {
                throw new Error(response.data.message)
            }
        } catch (err) {
            if (err.message === "Forbidden") {
                alert("Only admins can update user")
            } else {
                alert(err)
            }
        }
    }

    useEffect(() => {
        fetchservice.getUserInfo(id)
            .then((response) => {
                    setUser(response.data)
                }
            )
    }, [])

    return (
        <div className="user">
            <form className="form-horizontal">
                <div className="form-group row">
                    <label className="control-label col-sm-5">Firstname:</label>
                    <div className="col-sm-2">
                        <input
                            type={'text'}
                            value={user?.firstname}
                            onChange={(event) =>
                                setUser((prev) => ({...prev, firstname: event.target.value}))
                            }
                        />
                    </div>
                </div>
                <div className="form-group row">
                    <label className="control-label col-sm-5">Lastname: </label>
                    <div className="col-sm-2">
                        <input type={'text'}
                               value={user?.lastname}
                               onChange={(event) =>
                                   setUser((prev) => ({...prev, lastname: event.target.value}))
                        }
                        />
                    </div>
                </div>
                <div className="form-group row">
                    <label className="control-label col-sm-5">Email: </label>
                    <div className="col-sm-2">
                        <input type={'text'}
                               value={user?.email}
                               onChange={(event) =>
                                   setUser((prev) => ({...prev, email: event.target.value}))
                        }
                        />
                    </div>
                </div>
                <div className="form-group row">
                    <label className="control-label col-sm-5">Tickets: </label>
                    <div className="col-sm-2">
                        {user?.tickets.map(ticket => (
                            <div>
                                <Link to={`/sessions/${ticket.session_id}`}>
                                Ticket
                                </Link>
                            </div>
                            )
                        )}
                    </div>
                </div>
                <button className="btn btn-primary" type={'button'} onClick={updateUser}>Update</button>
                <Link to={'/users'}>
                    <input className="btn btn-danger" type={'button'} value="Back to list of users"/>
                </Link>
            </form>
        </div>
    )
}

export default User