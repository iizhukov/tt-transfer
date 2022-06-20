import { Link } from "react-router-dom";
import Button from "../ui/button/Button";
import Input from "../ui/input/Input";
import "./loginFields.scss";

const LoginFields = () => {
  return (
    <div className="wrap-of-register">
      <div className="registration-fields">
        <h1 className={"register-title"}>Войдите в свой аккаунт</h1>
        <div className={"register-sub-tittle"}>
          У вас еще нет аккаунта Трансфер?{" "}
          <Link
            to="/register"
            style={{ color: "blue", textDecoration: "none" }}
          >
            Создайте аккаунт
          </Link>
        </div>
        <Input placeholder={"E mail"} />
        <Input placeholder={"Пароль"} type={"password"} />
        <div className={"register-buttons"}>
          <Link to={"/"} style={{ textDecoration: "none" }}>
            <Button text={"ВОЙТИ"} callback={() => console.log("hello")} />
          </Link>
          <Link to={"/reset-password"}>
            <div
              style={{
                fontWeight: 400,
                fontSize: 16,
                textDecoration: "underline",
                color: "#787878",
                cursor: "pointer",
              }}
              className={"reset-password"}
            >
              Забыли пароль?
            </div>
          </Link>
        </div>
        <div className={"save-auth"}>
          <input type="text" type="checkbox" />
          <label>Запомнить меня?</label>
        </div>
      </div>
    </div>
  );
};

export default LoginFields;
