import "./scss/app.scss";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import Activity from "./pages/activity/Activity";
import Cars from "./pages/cars/Cars";
import Drivers from "./pages/drivers/Drivers";
import Login from "./pages/Login";
import PasswordReset from "./pages/passwordReset/PasswordReset";
import PasswordSent from "./pages/passwordSent/PasswordSent";
import Profile from "./pages/profile/Profile";
import Register from "./pages/Register";
import Request from "./pages/request/Request";
import Layout from "./components/layout/Layout";
import Tariffs from "./pages/tariffs/Tariffs";

function App() {
  return (
    <>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<Activity />} />
          <Route path="profile" element={<Profile />} />
          <Route path="requests" element={<Request />} />
          <Route path="drivers" element={<Drivers />} />
          <Route path="crm" element={<Request />} />
          <Route path="cars" element={<Cars />} />
          <Route path="tariffs" element={<Tariffs />} />
        </Route>
        <Route path="/password-sent" element={<PasswordSent />} />
        <Route path="/reset-password" element={<PasswordReset />} />
        <Route path="/register" element={<Register />} />
        <Route path="/login" element={<Login />} />
      </Routes>
    </>
  );
}

export default App;
