import { AnimatePresence, motion } from "framer-motion";
import { Link, Outlet } from "react-router-dom";
import burger from "../../assets/burger.svg";
import activeNewsIcon from "../../assets/icons8-rss-50 1.svg";
import notification from "../../assets/icons8-будильник-50 1.svg";
import searchIcon from "../../assets/icons8-поиск-50 1.svg";
import notActiveNewsIcon from "../../assets/not-active-news-icon.svg";
import userImage from "../../assets/Аватарка.svg";
import smallLogo from "../../assets/Логотип.svg";
import activeCrmIcon from "../../assets/active-crm-icon.svg";
import notActiveCrmIcon from "../../assets/icons8-crm-система-microsoft-dynamics-50 (1) 1.svg";

import { useEffect, useState } from "react";

import "./layout.scss";
import SidebarLink from "../sidebarLink/SidebarLink";

const Layout = () => {
  console.log("render layout");

  const [isVisibleSidebar, setIsVisibleSidebar] = useState(false);
  const [isVisibleUserInfo, setIsVisibleUserInfo] = useState(false);
  const [activeLinkIndex, setActiveLinkIndex] = useState(0);

  const handleVisibility = () => {
    setIsVisibleSidebar(!isVisibleSidebar);
  };

  const handleActiveLink = (id) => {
    setActiveLinkIndex(id);
  };

  const openSidebar = () => {
    localStorage.setItem("sidebar", "open");
  };
  const closeSidebar = () => {
    localStorage.setItem("sidebar", "close");
  };

  useEffect(() => {
    if (localStorage.getItem("sidebar") === "open") {
      setIsVisibleSidebar(true);
    } else {
      setIsVisibleSidebar(false);
    }
  }, []);

  const links = [
    {
      title: "Лента активности",
      activeIcon: activeNewsIcon,
      notActiveIcon: notActiveNewsIcon,
      isVisibleSidebar,
      handleActiveLink,
      path: "/",
    },
    {
      title: "CRM",
      activeIcon: activeCrmIcon,
      notActiveIcon: notActiveCrmIcon,
      isVisibleSidebar,
      handleActiveLink,
      path: "/crm",
    },
  ];

  return (
    <>
      <div className={"wrap-0f-top-menu"}>
        <div className="menu-blocks">
          <div className="menu-block">
            <img src={smallLogo} alt="" className={"small-logo"} />
            <AnimatePresence>
              {isVisibleSidebar && (
                <motion.div
                  initial={{ width: 0 }}
                  animate={{ width: 215 }}
                  exit={{ width: 0 }}
                  style={{ overflow: "hidden" }}
                  transition={{ type: "Tween" }}
                >
                  <div className={"full-logo"}>Трансфер</div>
                </motion.div>
              )}
            </AnimatePresence>
            <button
              className={
                isVisibleSidebar
                  ? " c-hamburger c-hamburger--htx is-active"
                  : "c-hamburger c-hamburger--htx"
              }
              onClick={async () => {
                await handleVisibility();
                if (isVisibleSidebar) {
                  closeSidebar();
                } else if (!isVisibleSidebar) {
                  openSidebar();
                }
              }}
            >
              <span>toggle menu</span>
            </button>
            <div className="global-search">
              <input
                type="text"
                className={"global-search-input"}
                placeholder={"Глобальный поиск"}
              />
              <img
                src={searchIcon}
                alt=""
                className="search-icon"
                onClick={() => alert("поиск начат")}
              />
            </div>
          </div>
          <div className="menu-block">
            <img src={notification} alt="" />
            <div className={"username"}>Вячеслав Терехов</div>
            <div
              className={"profile-image"}
              onClick={() => setIsVisibleUserInfo(!isVisibleUserInfo)}
            >
              <div>
                <img src={userImage} alt="" />
              </div>
            </div>
            {isVisibleUserInfo ? (
              <div className="user-info">
                <div className="user-info-image">
                  <img src={userImage} alt="" />
                </div>
                <div className="user-info-text">
                  <div className="user-name">Вячеслав</div>
                  <div className="user-email">goldweb56@yandex.ru</div>
                  <div className="userinfo-buttons">
                    <Link to="/profile" style={{ textDecoration: "none" }}>
                      <div>Мой профиль</div>
                    </Link>
                    <Link to="/login" style={{ textDecoration: "none" }}>
                      <div>Выход</div>
                    </Link>
                  </div>
                </div>
              </div>
            ) : null}
          </div>
        </div>
      </div>
      <div style={{ display: "flex" }}>
        <div className="wrap-of-sidebar">
          {links.map((link, index) => {
            return (
              <SidebarLink
                isVisibleSidebar={link.isVisibleSidebar}
                title={link.title}
                activeIcon={link.activeIcon}
                notActiveIcon={link.notActiveIcon}
                index={index}
                key={index}
                isActive={activeLinkIndex}
                handleActiveLink={handleActiveLink}
                path={link.path}
              />
            );
          })}
        </div>
        <div className="main-content">
          <Outlet />
        </div>
      </div>
    </>
  );
};

export default Layout;
