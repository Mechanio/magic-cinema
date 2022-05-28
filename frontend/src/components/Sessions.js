import React, {useState, useEffect} from 'react'
import { Link } from 'react-router-dom';
import fetchservice from "../services/fetch.service";

const Sessions = () => {
    const [sessions, setSessions] = useState([]);

    const fetchData = async () => {
        const res = await fetchservice.getSessionsInfo()
        setSessions(res.data)
    }

    const deleteSession = async (id_) => {
          try {
            const response = await fetchservice.deleteSession(id_)
            if(response && response.data && response.data.message === "Deleted") {
                await fetchData()
            } else {
                throw new Error(response.response.data.message)
            }
            } catch (err) {
                if(err.message === "Forbidden") {
                    alert("Only admins can delete session")
                } else {
                    alert(err)
                }
            }
    }

    useEffect(() => {
        fetchData()
    }, [])

    return (
        <div className="sessions">
            <table className="table table-striped table-hover">
                <tbody>
                    <tr>
                        <th className="text-center">Name</th>
                        <th className="text-center">View</th>
                        <th className="text-center">Delete</th>
                    </tr>
                    {sessions.map(session => (
                        <tr key={session.id}>
                            <td className="text-center">{`${session.movie.name} (${session.date})`}</td>
                            <td className="text-center">
                                <Link to={`/sessions/${session.id}`}>
                                    <input className="btn btn-primary" type="submit" value="View"/>
                                </Link>
                            </td>
                            <td className="text-center">
                                <a onClick={() => deleteSession(session.id)}>
                                    <input className="btn btn-danger" type="submit" value="Delete"/>
                                </a>
                            </td>
                        </tr>
                        )
                    )}
                </tbody>
            </table>
            <div className="text-center">
                <Link to={`/sessions/create`}>
                    <input className="btn btn-primary" type="submit" value="Create new session"/>
                </Link>
            </div>
        </div>
    )
}

export default Sessions
