import React, {useState, useEffect} from 'react'
import { Link } from 'react-router-dom';
import fetchservice from "../services/fetch.service";

const Directors = () => {
    const [directors, setDirectors] = useState([]);

    const fetchData = async () => {
        const res = await fetchservice.getDirectorsInfo()
        setDirectors(res.data)
    }

    const deleteDirector = async (id_) => {
          try {
            const response = await fetchservice.deleteDirector(id_)
            if(response && response.data && response.data.message === "Deleted") {
                await fetchData()
            } else {
                throw new Error(response.response.data.message)
            }
            } catch (err) {
                if(err.message === "Forbidden") {
                    alert("Only admins can delete director")
                } else {
                    alert(err)
                }
            }
    }

    useEffect(() => {
        fetchData()
    }, [])

    return (
        <div className="directors">
            <table className="table table-striped table-hover">
                <tbody>
                    <tr>
                        <th className="text-center">Name</th>
                        <th className="text-center">View</th>
                        <th className="text-center">Delete</th>
                    </tr>
                    {directors.map(director => (
                        <tr key={director.id}>
                            <td className="text-center">{director.firstname + ' ' + director.lastname}</td>
                            <td className="text-center">
                                <Link to={`/directors/${director.id}`}>
                                    <input className="btn btn-primary" type="submit" value="View"/>
                                </Link>
                            </td>
                            <td className="text-center">
                                <a onClick={() => deleteDirector(director.id)}>
                                    <input className="btn btn-danger" type="submit" value="Delete"/>
                                </a>
                            </td>
                        </tr>
                        )
                    )}
                </tbody>

            </table>
            <div className="text-center">
                <Link to={`/directors/create`}>
                    <input className="btn btn-primary" type="submit" value="Create new director"/>
                </Link>
            </div>
        </div>
    )
}

export default Directors
