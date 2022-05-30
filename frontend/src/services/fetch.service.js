import axios from "axios"

const getProfileInfo = () => {
    return axios.get("http://localhost:5000/api/users/current")
}


const getActorsInfo = () => {
    return axios.get("http://localhost:5000/api/actors/")
}

const getActorInfo = (id_) => {
    return axios.get("http://localhost:5000/api/actors/" + id_)
}

const deleteActor = (id_) => {
    return axios.delete("http://localhost:5000/api/actors/" + id_)
}

const createActor = (firstname, lastname) => {
    return axios.post("http://localhost:5000/api/actors/", {firstname, lastname})
}

const updateActor = (id_, firstname, lastname) => {
    return axios.patch("http://localhost:5000/api/actors/" + id_, {firstname, lastname})
}


const getMoviesInfo = () => {
    return axios.get("http://localhost:5000/api/movies/")
}

const getMovieInfo = (id_) => {
    return axios.get("http://localhost:5000/api/movies/" + id_)
}

const deleteMovie = (id_) => {
    return axios.delete("http://localhost:5000/api/movies/" + id_)
}

const createMovie = (name, description, director_id, year, month, day, genres, actors) => {
    return axios.post("http://localhost:5000/api/movies/", {name, description, director_id, year, month, day, genres, actors})
}

const updateMovie = (id_, name, description, director_id, genres, actors) => {
    return axios.patch("http://localhost:5000/api/movies/" + id_, {name, description, director_id, genres, actors})
}

const getMovieInfoByName = (name) => {
    return axios.get(`http://localhost:5000/api/movies/?name=${name}`)
}


const getGenresInfo = () => {
    return axios.get("http://localhost:5000/api/genres/")
}

const deleteGenre = (id_) => {
    return axios.delete("http://localhost:5000/api/genres/" + id_)
}

const getGenreInfo = (id_) => {
    return axios.get("http://localhost:5000/api/genres/" + id_)
}

const updateGenre = (id_, genre) => {
    return axios.patch("http://localhost:5000/api/genres/" + id_, {genre})
}

const createGenre = (genre) => {
    return axios.post("http://localhost:5000/api/genres/", {genre})
}


const getDirectorsInfo = () => {
    return axios.get("http://localhost:5000/api/director/")
}

const deleteDirector = (id_) => {
    return axios.delete("http://localhost:5000/api/director/" + id_)
}

const getDirectorInfo = (id_) => {
    return axios.get("http://localhost:5000/api/director/" + id_)
}

const updateDirector = (id_, firstname, lastname) => {
    return axios.patch("http://localhost:5000/api/director/" + id_, {firstname, lastname})
}

const createDirector = (firstname, lastname) => {
    return axios.post("http://localhost:5000/api/director/", {firstname, lastname})
}

const getDirectorInfoByName = (firstname, lastname) => {
    return axios.get(`http://localhost:5000/api/director/?firstname=${firstname}&lastname=${lastname}`)
}


const getUsersInfo = () => {
    return axios.get("http://localhost:5000/api/users/")
}

const deleteUser = (id_) => {
    return axios.delete("http://localhost:5000/api/users/" + id_)
}

const getUserInfo = (id_) => {
    return axios.get("http://localhost:5000/api/users/" + id_)
}

const updateUser = (id_, firstname, lastname, email) => {
    return axios.patch("http://localhost:5000/api/users/" + id_, {firstname, lastname, email})
}

const createUser = (firstname, lastname, email, password, is_admin) => {
    return axios.post("http://localhost:5000/api/users/", {firstname, lastname, email, password, is_admin})
}

const getInactiveUsersInfo = () => {
    return axios.get("http://localhost:5000/api/users/inactive")
}


const getSessionsInfo = () => {
    return axios.get("http://localhost:5000/api/sessions/")
}

const deleteSession = (id_) => {
    return axios.delete("http://localhost:5000/api/sessions/" + id_)
}

const createSession = (movie_id, auditorium_id, year, month, day, hour, minute) => {
    return axios.post("http://localhost:5000/api/sessions/", {movie_id, auditorium_id, year, month, day, hour, minute})
}

const getSessionInfo = (id_) => {
    return axios.get("http://localhost:5000/api/sessions/" + id_)
}


const buyTicket = (session_id) => {
    return axios.post("http://localhost:5000/api/tickets/", {session_id})
}


const getAuditoriumsInfo = () => {
    return axios.get("http://localhost:5000/api/auditorium/")
}

const deleteAuditorium = (id_) => {
    return axios.delete("http://localhost:5000/api/auditorium/" + id_)
}

const createAuditorium = (seats) => {
    return axios.post("http://localhost:5000/api/auditorium/", {seats})
}

const fetchservice = {
    getProfileInfo,
    getActorsInfo,
    getActorInfo,
    deleteActor,
    createActor,
    updateActor,
    getMoviesInfo,
    getMovieInfo,
    deleteMovie,
    createMovie,
    updateMovie,
    getMovieInfoByName,
    getGenresInfo,
    deleteGenre,
    getGenreInfo,
    updateGenre,
    createGenre,
    getDirectorsInfo,
    deleteDirector,
    getDirectorInfo,
    updateDirector,
    createDirector,
    getDirectorInfoByName,
    getUsersInfo,
    deleteUser,
    getUserInfo,
    updateUser,
    createUser,
    getInactiveUsersInfo,
    getSessionsInfo,
    deleteSession,
    createSession,
    getSessionInfo,
    buyTicket,
    getAuditoriumsInfo,
    deleteAuditorium,
    createAuditorium
}

export default fetchservice