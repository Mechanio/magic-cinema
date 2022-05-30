import React, {useState, useEffect} from 'react'
import { Link } from 'react-router-dom';
import fetchservice from "../services/fetch.service";

const Movies = () => {
    const [movies, setMovies] = useState([]);

    const fetchData = async () => {
        const res = await fetchservice.getMoviesInfo()
        setMovies(res.data)
    }

    const deleteMovie = async (id_) => {
          try {
            const response = await fetchservice.deleteMovie(id_)
            if(response && response.data && response.data.message === "Deleted") {
                await fetchData()
            } else {
                throw new Error(response.response.data.message)
            }
            } catch (err) {
                if(err.message === "Forbidden") {
                    alert("Only admins can delete movie")
                } else {
                    alert(err)
                }
            }
    }

    useEffect(() => {
        fetchData()
    }, [])

    return (
        <div className="movies">
            <table className="table table-striped table-hover">
                <tbody>
                    <tr>
                        <th className="text-center">Name</th>
                        <th className="text-center">View</th>
                        <th className="text-center">Delete</th>
                    </tr>
                    {movies.map(movie => (
                        <tr key={movie.id}>
                            <td className="text-center">{movie.name}</td>
                            <td className="text-center">
                                <Link to={`/movies/${movie.id}`}>
                                    <input className="btn btn-primary" type="submit" value="View"/>
                                </Link>
                            </td>
                            <td className="text-center">
                                <a onClick={() => deleteMovie(movie.id)}>
                                    <input className="btn btn-danger" type="submit" value="Delete"/>
                                </a>
                            </td>
                        </tr>
                        )
                    )}
                </tbody>

            </table>
            <div className="text-center">
                <Link to={`/movies/create`}>
                    <input className="btn btn-primary" type="submit" value="Create new movie"/>
                </Link>
            </div>
        </div>
    )
}

export default Movies
