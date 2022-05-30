import React, {useState, useEffect} from 'react'
import { Link } from 'react-router-dom';
import fetchservice from "../services/fetch.service";

const Auditoriums = () => {
    const [auditoriums, setAuditoriums] = useState([]);

    const fetchData = async () => {
        const res = await fetchservice.getAuditoriumsInfo()
        setAuditoriums(res.data)
    }

    const deleteAuditorium = async (id_) => {
          try {
            const response = await fetchservice.deleteAuditorium(id_)
            if(response && response.data && response.data.message === "Deleted") {
                await fetchData()
            } else {
                throw new Error(response.response.data.message)
            }
            } catch (err) {
                if(err.message === "Forbidden") {
                    alert("Only admins can delete auditorium")
                } else {
                    alert(err)
                }
            }
    }

    useEffect(() => {
        fetchData()
    }, [])

    return (
        <div className="auditoriums">
            <table className="table table-striped table-hover">
                <tbody>
                    <tr>
                        <th className="text-center">Information</th>
                        <th className="text-center">Delete</th>
                    </tr>
                    {auditoriums.map(auditorium => (
                        <tr key={auditorium.id}>
                            <td className="text-center">{`ID: ${auditorium.id} Seats: ${auditorium.seats}`}</td>
                            <td className="text-center">
                                <a onClick={() => deleteAuditorium(auditorium.id)}>
                                    <input className="btn btn-danger" type="submit" value="Delete"/>
                                </a>
                            </td>
                        </tr>
                        )
                    )}
                </tbody>

            </table>
            <div className="text-center">
                <Link to={`/auditoriums/create`}>
                    <input className="btn btn-primary" type="submit" value="Create new auditorium"/>
                </Link>
            </div>
        </div>
    )
}

export default Auditoriums
