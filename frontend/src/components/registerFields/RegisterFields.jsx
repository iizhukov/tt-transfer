import { Link, useNavigate } from "react-router-dom";
import "../loginFields/loginFields.scss";
import Button from "../ui/button/Button";
import Input from "../ui/input/Input";
import "./registerFields.scss";

const RegisterFields = () => {
  const navigate = useNavigate();

  return (
    <div className="wrap-of-register">
      <div className="registration-fields">
        <h1 className={"register-title"}>Регистрация</h1>
        <div className={"register-sub-tittle"}>
          Создайте аккаунт Трансфер и получите все необходимые инструменты
          эффективного управления бизнесом! У вас уже есть аккаунт Трансфер?
          <Link to="/login" style={{ color: "blue", textDecoration: "none" }}>
            {" "}
            Войти в аккаунт
          </Link>
        </div>
        <Input placeholder={"Выберите роль"} />
        <Input placeholder={"Ваше имя"} />
        <Input placeholder={"E mail"} />
        <Input placeholder={"Телефон"} />
        <Input placeholder={"Пароль"} type={"password"} />
        <Input placeholder={"Повторите пароль"} type={"password"} />
        <div className={"register-buttons"} style={{ marginTop: 25 }}>
          <Button text={"РЕГИСТРАЦИЯ"} callback={() => navigate("/news")} />
        </div>
        <p>
          Регистрируясь, вы принимаете{" "}
          <span className={"blue"}>лицензионное соглашение</span>
        </p>
      </div>
    </div>
  );
};

export default RegisterFields;
