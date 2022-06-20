import Button from "../ui/button/Button";
import CustomEditProfileInput from "./CustomEditProfileInput";

const ProfileAccount = () => {
  return (
    <>
      <CustomEditProfileInput
        label={"Логин (e-mail)"}
        value={"goldweb56@yandex.ru"}
      />
      <CustomEditProfileInput
        label={"Номер телефона"}
        value={"+7 (987) 119-50-28"}
      />
      <CustomEditProfileInput label={"Фамилия"} value={"Терехов"} />
      <CustomEditProfileInput label={"Имя"} value={"Вячеслав"} />
      <CustomEditProfileInput label={"Отчество"} value={"Александрович"} />

      <Button text={"Сохранить"} style={{ fontWeight: 300, marginTop: 40 }} />
    </>
  );
};

export default ProfileAccount;
