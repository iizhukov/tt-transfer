import { duration } from "@mui/material";
import { AnimatePresence, motion } from "framer-motion";
import "../layout/layout.scss";
import { useNavigate, NavLink } from "react-router-dom";
import { useState } from "react";
import CustomSidebarLink from "../customSidebarLink/CustomSidebarLink";

const SidebarLink = ({
  isVisibleSidebar,
  activeIcon,
  notActiveIcon,
  title,
  isActive,
  index,
  handleActiveLink,
  path,
}) => {
  const navigate = useNavigate();

  const subLink = [
    {
      title: "Заявки",
      path: "/requests",
    },
    {
      title: "Водители",
      path: "/drivers",
    },
    {
      title: "Машины",
      path: "/cars",
    },
    {
      title: "Тарифы",
      path: "/tariffs",
    },
  ];
  return (
    <>
      <CustomSidebarLink to={path}>
        <div
          style={
            isActive === index
              ? { background: "rgba(149, 159, 173, 0.3)" }
              : null
          }
          onClick={() => {
            handleActiveLink(index);
          }}
          className={"sidebar-item"}
        >
          <div className="sidebar-icon-wrap">
            <img
              src={isActive === index ? activeIcon : notActiveIcon}
              alt=""
              className="sidebar-icon"
            />
            {isActive === index && (
              <AnimatePresence>
                <motion.div
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  exit={{ opacity: 0 }}
                  style={{ overflow: "hidden" }}
                >
                  <div className="active-indicator"></div>
                </motion.div>
              </AnimatePresence>
            )}
          </div>
          <AnimatePresence>
            {isVisibleSidebar && (
              <motion.div
                initial={{ width: 0 }}
                animate={{ width: 220 }}
                exit={{ width: 0 }}
                style={{ overflow: "hidden" }}
                transition={{ type: "Tween" }}
              >
                <div
                  className={"link-title"}
                  style={isActive !== index ? { color: "#B4BCC8" } : null}
                >
                  {title}
                </div>
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      </CustomSidebarLink>

      {isActive === index && isActive && isVisibleSidebar
        ? subLink.map((link, pos) => (
            <AnimatePresence>
              {isVisibleSidebar && (
                <motion.div
                  initial={{ width: 0 }}
                  animate={{ width: "auto" }}
                  exit={{ width: 0 }}
                  style={{ overflow: "hidden" }}
                  transition={{ type: "Tween" }}
                >
                  <CustomSidebarLink
                    to={link.path}
                    style={{ textDecoration: "none" }}
                  >
                    <div className={`sidebar-item`} key={pos}>
                      <div className="sidebar-icon-wrap"></div>
                      <div
                        className={"link-title"}
                        style={isActive !== index ? { color: "#B4BCC8" } : null}
                      >
                        {link.title}
                      </div>
                    </div>
                  </CustomSidebarLink>
                </motion.div>
              )}
            </AnimatePresence>
          ))
        : null}
    </>
  );
};

export default SidebarLink;
