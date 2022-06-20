import "./button.scss";

const Button = ({ width = 220, height = 55, text, callback, style }) => {
  return (
    <button
      className={"enter-button"}
      onClick={callback}
      style={{ width, height, ...style }}
    >
      {text}
    </button>
  );
};

export default Button;
