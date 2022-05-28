import React, {useState, useEffect} from 'react'
import { Link } from 'react-router-dom';
import fetchservice from "../services/fetch.service";

const Users = () => {
    const [users, setUsers] = useState([]);

    const fetchData = async () => {
        const res = await fetchservice.getUsersInfo()
        setUsers(res.data)
    }

    const deleteUser = async (id_) => {
          try {
            const response = await fetchservice.deleteUser(id_)
            if(response && response.data && response.data.message === "Deleted") {
                await fetchData()
            } else {
                throw new Error(response.response.data.message)
            }
            } catch (err) {
                if(err.message === "Forbidden") {
                    alert("Only admins can delete user")
                } else {
                    alert(err)
                }
            }
    }

    useEffect(() => {
        fetchData()
    }, [])

    return (
        <div className="users">
            <table className="table table-striped table-hover">
                <tbody>
                    <tr>
                        <th className="text-center">Name</th>
                        <th className="text-center">View</th>
                        <th className="text-center">Delete</th>
                    </tr>
                    {users.map(user => (
                        <tr key={user.id}>
                            <td className="text-center">{user.firstname + ' ' + user.lastname}</td>
                            <td className="text-center">
                                <Link to={`/users/${user.id}`}>
                                    <input className="btn btn-primary" type="submit" value="View"/>
                                </Link>
                            </td>
                            <td className="text-center">
                                <a onClick={() => deleteUser(user.id)}>
                                    <input className="btn btn-danger" type="submit" value="Delete"/>
                                </a>
                            </td>
                        </tr>
                        )
                    )}
                </tbody>

            </table>
            <div className="text-center">
                <Link to={`/users/create`}>
                    <input className="btn btn-primary" type="submit" value="Create new user"/>
                </Link>
            </div><br />
            <div className="text-center">
                <Link to={`/users/inactive`}>
                    <input className="btn btn-primary" type="submit" value="View deleted users"/>
                </Link>
            </div>
        </div>
    )
}

export default Users
