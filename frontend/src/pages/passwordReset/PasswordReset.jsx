import Logo from "../../components/logo/Logo";
import "../../components/loginFields/loginFields.scss";
import Button from "../../components/ui/button/Button";
import Input from "../../components/ui/input/Input";
import { useNavigate } from "react-router-dom";

const PasswordReset = () => {
  const navigate = useNavigate();

  return (
    <>
      <Logo />
      <div className="wrap-of-register">
        <div className="registration-fields">
          <h1 className={"register-title"}>Введите свой e-mail</h1>
          <div className={"register-sub-tittle"}>
            На указанный адрес мы вышлем новый пароль{" "}
          </div>
          <Input placeholder={"E mail"} />
          <div
            style={{
              display: "flex",
              justifyContent: "space-between",
              alignItems: "flex-end",
            }}
          >
            <Button
              text={"ОТПРАВИТЬ"}
              callback={() => navigate("/password-sent")}
              style={{ fontWeight: 300, marginTop: 30 }}
            />
            <div
              style={{
                fontWeight: 300,
                fontSize: 16,
                textDecoration: "underline",
                color: "#787878",
                cursor: "pointer",
                marginTop: 10,
              }}
              className={"reset-password"}
              onClick={() => navigate("/login")}
            >
              Страница входа
            </div>
          </div>
        </div>
      </div>
    </>
  );
};

export default PasswordReset;
