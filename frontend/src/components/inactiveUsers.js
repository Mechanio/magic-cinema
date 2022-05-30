import React, {useState, useEffect} from 'react'
import { Link } from 'react-router-dom';
import fetchservice from "../services/fetch.service";

const InactiveUsers = () => {
    const [users, setUsers] = useState([]);

    const fetchData = async () => {
        const res = await fetchservice.getInactiveUsersInfo()
        setUsers(res.data)
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
                    </tr>
                    {users.map(user => (
                        <tr key={user.id}>
                            <td className="text-center">{user.firstname + ' ' + user.lastname}</td>
                        </tr>
                        )
                    )}
                </tbody>

            </table>
            <div className="text-center">
                <Link to={`/users`}>
                    <input className="btn btn-primary" type="submit" value="Back to users list"/>
                </Link>
            </div>
        </div>
    )
}

export default InactiveUsers
