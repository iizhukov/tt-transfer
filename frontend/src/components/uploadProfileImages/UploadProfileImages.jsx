import "./uploadProfileImages.scss";
import { Button, Input } from "@mui/material";
import passport from "../../assets/pasport.png";
import drive from "../../assets/drive.png";

const UploadProfileImages = () => {
  return (
    <div>
      <div style={{ marginBottom: 15 }}>Аватарка</div>
      <label htmlFor="contained-button-file">
        <Input
          accept="image/*"
          id="contained-button-file"
          multiple
          type="file"
          style={{ display: "none" }}
        />
        <Button
          variant="contained"
          component="span"
          sx={{
            fontWeight: 300,
            textTransform: "none",
            background: "#E8E8E8",
            boxShadow: "none",
            color: "#000",
            height: 40,
            width: 150,
          }}
        >
          Выберите файл
        </Button>
        <span style={{ marginLeft: 15 }}>Файл не выбран</span>
      </label>
      <div style={{ marginBottom: 15, marginTop: 25 }}>Скан-копии</div>
      <Button
        variant="contained"
        component="span"
        sx={{
          fontWeight: 300,
          textTransform: "none",
          background: "#E8E8E8",
          boxShadow: "none",
          color: "#000",
          height: 40,
          width: 150,
        }}
      >
        Pasport.png
      </Button>
      <span style={{ marginLeft: 15 }}>Загрузка 85%</span>

      <div className="documents">
        <img src={passport} alt="" />
        <img src={drive} alt="" />
      </div>

      <button className={"enter-button-1"}>Сохранить</button>
    </div>
  );
};

export default UploadProfileImages;
