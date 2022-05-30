import React, {useState} from 'react'
import { useNavigate } from "react-router-dom";
import authService from "../services/auth.service";

export default function Login() {
    const [email, setEmail] = useState("")
    const [password, setPassword] = useState("")
    const [error, setError] = useState(null)
    const navigate = useNavigate()

    const handleClick = async (event) => {
        event.preventDefault()

        try {
           const response = await authService.login(email, password)
            if (response && response.data && response.data.access_token) {
                localStorage.setItem("user", JSON.stringify(response.data));
                navigate('/profile')
                return response.data;
            } else {
                throw new Error(response.response.data.message)
            }
        } catch(err) {
            setError(err.message)
        }
    }

    return (
        <div className="login">
            {error && <p style={{color: 'red'}}>{error}</p>}
            <form className="form-horizontal" onSubmit={handleClick}>
                <div className="text-center">
                    <div className="form-group row">
                        <label className="control-label col-sm-5">Email: </label>
                        <div className="col-sm-2">
                            <input className="form-control" type="email" value={email}
                                   onChange={(e) => setEmail(e.target.value)}/>
                        </div>
                    </div>
                    <div className="form-group row">
                        <label className="control-label col-sm-5">Password: </label>
                        <div className="col-sm-2">
                            <input className="form-control" type="password" value={password}
                                   onChange={(e) => setPassword(e.target.value)}/>
                        </div>
                    </div>
                    <button className="btn btn-primary" type="submit">Login</button>
                </div>
            </form>
        </div>
    )
}
