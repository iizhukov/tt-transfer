import "./profileAccount.scss";
import { useState } from "react";
import Button from "../ui/button/Button";
import CustomEditProfileInput from "./CustomEditProfileInput";

const ChangePassword = () => {
  const [showOldPassword, setShowOldPassword] = useState(false);
  const [showNewPassword, setShowNewPassword] = useState(false);
  const [showPassword, setShowPassword] = useState(false);
  const [oldPassword, setOldPassword] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [newPasswordRepeat, setNewPasswordRepeat] = useState("");

  return (
    <>
      <div className={"change-password-input"}>
        <div style={{ color: "#777777" }}>Старый пароль</div>

        <input
          type={showOldPassword ? "text" : "password"}
          value={oldPassword}
          onChange={(e) => {
            setOldPassword(e.target.value);
          }}
          placeholder={"Введите старый пароль"}
          className={"edit-profile-input"}
          style={{ marginBottom: 15 }}
          autoComplete={"off"}
        />
        {oldPassword.length !== 0 && (
          <div
            onClick={() => setShowOldPassword(!showOldPassword)}
            className={"show-password"}
          >
            {!showOldPassword ? "Показать" : "Скрыть"}
          </div>
        )}
      </div>
      <div className={"change-password-input"}>
        <div style={{ color: "#777777" }}>Новый пароль</div>

        <input
          type={showPassword ? "text" : "password"}
          value={newPassword}
          onChange={(e) => {
            setNewPassword(e.target.value);
          }}
          placeholder={"Введите пароль"}
          className={"edit-profile-input"}
          style={{ marginBottom: 15 }}
          autoComplete={"off"}
        />
        {newPassword.length !== 0 && (
          <div
            onClick={() => setShowPassword(!showPassword)}
            className={"show-password"}
          >
            {!showPassword ? "Показать" : "Скрыть"}
          </div>
        )}
      </div>
      <div className={"change-password-input"}>
        <div style={{ color: "#777777" }}>Повторите новый пароль</div>

        <input
          type={showNewPassword ? "text" : "password"}
          value={newPasswordRepeat}
          onChange={(e) => {
            setNewPasswordRepeat(e.target.value);
          }}
          placeholder={"Введите пароль"}
          className={"edit-profile-input"}
          style={{ marginBottom: 15 }}
          autoComplete={"off"}
        />
        {newPasswordRepeat.length !== 0 && (
          <div
            onClick={() => setShowNewPassword(!showNewPassword)}
            className={"show-password"}
          >
            {!showNewPassword ? "Показать" : "Скрыть"}
          </div>
        )}
      </div>

      <Button
        text={"Сохранить"}
        height={45}
        width={180}
        style={{ marginTop: 64 }}
      />
    </>
  );
};

export default ChangePassword;
