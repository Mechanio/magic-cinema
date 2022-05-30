import React, {useState, useEffect} from 'react'
import { Link } from 'react-router-dom';
import fetchservice from "../services/fetch.service";

const Actors = () => {
    const [actors, setActors] = useState([]);

    const fetchData = async () => {
        const res = await fetchservice.getActorsInfo()
        setActors(res.data)
    }

    const deleteActor = async (id_) => {
          try {
            const response = await fetchservice.deleteActor(id_)
            if(response && response.data && response.data.message === "Deleted") {
                await fetchData()
            } else {
                throw new Error(response.response.data.message)
            }
            } catch (err) {
                if(err.message === "Forbidden") {
                    alert("Only admins can delete actor")
                } else {
                    alert(err)
                }
            }
    }

    useEffect(() => {
        fetchData()
    }, [])

    return (
        <div className="actors">
            <table className="table table-striped table-hover">
                <tbody>
                    <tr>
                        <th className="text-center">Name</th>
                        <th className="text-center">View</th>
                        <th className="text-center">Delete</th>
                    </tr>
                    {actors.map(actor => (
                        <tr key={actor.id}>
                            <td className="text-center">{actor.firstname + ' ' + actor.lastname}</td>
                            <td className="text-center">
                                <Link to={`/actors/${actor.id}`}>
                                    <input className="btn btn-primary" type="submit" value="View"/>
                                </Link>
                            </td>
                            <td className="text-center">
                                <a onClick={() => deleteActor(actor.id)}>
                                    <input className="btn btn-danger" type="submit" value="Delete"/>
                                </a>
                            </td>
                        </tr>
                        )
                    )}
                </tbody>

            </table>
            <div className="text-center">
                <Link to={`/actors/create`}>
                    <input className="btn btn-primary" type="submit" value="Create new user"/>
                </Link>
            </div>
        </div>
    )
}

export default Actors
