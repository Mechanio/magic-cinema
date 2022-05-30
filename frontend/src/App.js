import React, {useEffect} from 'react'
import 'bootstrap/dist/css/bootstrap.css'
import MyNavbar from './Navbar'
import Login from './Auth/Login'
import Profile from './Profile'
import Actors from './components/Actors'
import Actor from './components/Actor'
import CreateActor from './components/createActor'
import Movies from './components/Movies'
import Movie from './components/Movie'
import { Route, Routes, useLocation, useNavigate } from "react-router-dom"
import authService from "./services/auth.service"
import CreateMovie from "./components/createMovie"
import UpdateMovie from "./components/updateMovie"
import Genres from "./components/Genres"
import Genre from "./components/Genre"
import CreateGenre from "./components/createGenre"
import Directors from "./components/Directors"
import Director from "./components/Director"
import CreateDirector from "./components/createDirector"
import Users from "./components/Users"
import User from "./components/User"
import CreateUser from "./components/createUser"
import InactiveUsers from "./components/inactiveUsers"
import Sessions from "./components/Sessions"
import Session from "./components/Session"
import CreateSession from "./components/createSession"
import NotFound from "./components/NotFound";
import Auditoriums from "./components/Auditoriums"
import CreateAuditorium from "./components/createAuditorium"


function App() {
    const { pathname } = useLocation()
    const navigate = useNavigate()

    useEffect(() => {
        authService.authGuard(pathname, navigate)
    }, [pathname])

    return (
        <div>
            <MyNavbar/>
            <div className="content">
                <Routes>
                    <Route exact path="/"/>
                    <Route exact path="/auth/login" element={<Login/>}/>
                    <Route exact path="/profile" element={<Profile/>}/>
                    <Route exact path="/movies" element={<Movies/>}/>
                    <Route exact path="/movies/:id" element={<Movie/>}/>
                    <Route exact path="/movies/:id/edit" element={<UpdateMovie/>}/>
                    <Route exact path="/movies/create" element={<CreateMovie/>}/>
                    <Route exact path="/actors" element={<Actors/>}/>
                    <Route exact path="/actors/:id" element={<Actor/>}/>
                    <Route exact path="/actors/create" element={<CreateActor/>}/>
                    <Route exact path="/genres" element={<Genres/>}/>
                    <Route exact path="/genres/:id" element={<Genre/>}/>
                    <Route exact path="/genres/create" element={<CreateGenre/>}/>
                    <Route exact path="/directors" element={<Directors/>}/>
                    <Route exact path="/directors/:id" element={<Director/>}/>
                    <Route exact path="/directors/create" element={<CreateDirector/>}/>
                    <Route exact path="/users" element={<Users/>}/>
                    <Route exact path="/users/:id" element={<User/>}/>
                    <Route exact path="/users/create" element={<CreateUser/>}/>
                    <Route exact path="/users/inactive" element={<InactiveUsers/>}/>
                    <Route exact path="/sessions" element={<Sessions/>}/>
                    <Route exact path="/sessions/:id" element={<Session/>}/>
                    <Route exact path="/sessions/create" element={<CreateSession/>}/>
                    <Route exact path="/auditoriums" element={<Auditoriums/>}/>
                    <Route exact path="/auditoriums/create" element={<CreateAuditorium/>}/>
                    <Route exact path="*" element={<NotFound/>}/>
                </Routes>
            </div>
        </div>
    )
}

export default App;
