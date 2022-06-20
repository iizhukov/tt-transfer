import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter } from "react-router-dom";
import App from "./App";
import Login from "./pages/Login";
import Activity from "./pages/activity/Activity";
import PasswordReset from "./pages/passwordReset/PasswordReset";
import Profile from "./pages/profile/Profile";
import PasswordSent from "./pages/passwordSent/PasswordSent";
import Register from "./pages/Register";
import Request from "./pages/request/Request";
import "./scss/index.scss";

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(
  <BrowserRouter>
    {/*<React.StrictMode>*/}
    <App />
    {/*</React.StrictMode>*/}
  </BrowserRouter>
);
