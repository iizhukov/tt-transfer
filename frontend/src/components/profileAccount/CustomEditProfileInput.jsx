import "./profileAccount.scss";

const CustomEditProfileInput = ({ value, label, type = "text" }) => {
  return (
    <div className={"edit-profile-input-item"}>
      <div style={{ color: "#777777" }}>{label}</div>
      <input
        type={type}
        className={"edit-profile-input"}
        placeholder={value}
        autoComplete={"off"}
      />
    </div>
  );
};

export default CustomEditProfileInput;
