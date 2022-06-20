import { useState } from "react";
import Layout from "../../components/layout/Layout";
import profile from "../../assets/profile-avatar.svg";
import activeSettings from "../../assets/settings.svg";
import changePassword from "../../assets/change-password.svg";
import logout from "../../assets/logout.svg";
import addPhoto from "../../assets/add-photo-profile.svg";
import activeLogout from "../../assets/icons8-выход-10.png";
import activeChangePassword from "../../assets/active-change-password.svg";
import activeAddPhoto from "../../assets/active-add-photo.svg";
import settings from "../../assets/set.svg";
import "./profile.scss";
import ChangePassword from "../../components/profileAccount/ChangePassword";
import ProfileAccount from "../../components/profileAccount/ProfileAccount";
import UploadProfileImages from "../../components/uploadProfileImages/UploadProfileImages";
import { useNavigate } from "react-router-dom";

const Profile = () => {
  const [activeLink, setActiveLink] = useState(0);

  const navigate = useNavigate();

  return (
    <>
      <div className="profile-wrap">
        <div className="profile-control">
          <div className="profile-image">
            <img src={profile} alt="" />
          </div>
          <div
            className={`profile-link-item ${activeLink === 0 && "active"}`}
            onClick={() => setActiveLink(0)}
          >
            <div className="icon">
              <img src={activeLink === 0 ? activeSettings : settings} alt="" />
            </div>
            <div className={`profile-link-item-text`}>Аккаунт</div>
          </div>
          <div
            className={`profile-link-item ${activeLink === 1 && "active"}`}
            onClick={() => setActiveLink(1)}
          >
            <div className="icon">
              <img
                src={activeLink === 1 ? activeChangePassword : changePassword}
                alt=""
              />
            </div>
            <div className={`profile-link-item-text`}>Изменение пароля</div>
          </div>
          <div
            className={`profile-link-item ${activeLink === 2 && "active"}`}
            onClick={() => setActiveLink(2)}
          >
            <div className="icon">
              <img src={activeLink === 2 ? activeAddPhoto : addPhoto} alt="" />
            </div>
            <div className={`profile-link-item-text`}>Фотографии</div>
          </div>
          <div
            className={`profile-link-item `}
            onClick={() => navigate("/login")}
          >
            <div className="icon">
              <img src={logout} alt="" />
            </div>
            <div className={`profile-link-item-text`}>Выход из системы</div>
          </div>
        </div>
        <div className="profile-data">
          {activeLink === 0 && <ProfileAccount />}
          {activeLink === 1 && <ChangePassword />}
          {activeLink === 2 && <UploadProfileImages />}
        </div>
      </div>
    </>
  );
};

export default Profile;
