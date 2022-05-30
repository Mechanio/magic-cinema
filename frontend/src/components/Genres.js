import React, {useState, useEffect} from 'react'
import { Link } from 'react-router-dom';
import fetchservice from "../services/fetch.service";

const Genres = () => {
    const [genres, setGenres] = useState([]);

    const fetchData = async () => {
        const res = await fetchservice.getGenresInfo()
        setGenres(res.data)
    }

    const deleteGenre = async (id_) => {
          try {
            const response = await fetchservice.deleteGenre(id_)
            if(response && response.data && response.data.message === "Deleted") {
                await fetchData()
            } else {
                throw new Error(response.response.data.message)
            }
            } catch (err) {
                if(err.message === "Forbidden") {
                    alert("Only admins can delete genre")
                } else {
                    alert(err)
                }
            }
    }

    useEffect(() => {
        fetchData()
    }, [])

    return (
        <div className="genres">
            <table className="table table-striped table-hover">
                <tbody>
                    <tr>
                        <th className="text-center">Name</th>
                        <th className="text-center">View</th>
                        <th className="text-center">Delete</th>
                    </tr>
                    {genres.map(genre => (
                        <tr key={genre.id}>
                            <td className="text-center">{genre.genre}</td>
                            <td className="text-center">
                                <Link to={`/genres/${genre.id}`}>
                                    <input className="btn btn-primary" type="submit" value="View"/>
                                </Link>
                            </td>
                            <td className="text-center">
                                <a onClick={() => deleteGenre(genre.id)}>
                                    <input className="btn btn-danger" type="submit" value="Delete"/>
                                </a>
                            </td>
                        </tr>
                        )
                    )}
                </tbody>

            </table>
            <div className="text-center">
                <Link to={`/genres/create`}>
                    <input className="btn btn-primary" type="submit" value="Create new genre"/>
                </Link>
            </div>
        </div>
    )
}

export default Genres
