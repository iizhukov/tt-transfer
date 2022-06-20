import "./tabs.scss";
import { useState } from "react";

const Tabs = ({ items }) => {
  const [activeTab, setActiveTab] = useState(0);

  const handleClick = (index) => {
    setActiveTab(index);
  };

  const tabs = [
    {
      title: "Текущие",
    },
    {
      title: "Архив",
    },
    {
      title: "Калькулятор",
    },
  ];

  return (
    <div className="tabs-wrapper">
      {tabs.map((tab, index) => (
        <div key={index}>
          <div
            className={`tab-item ${activeTab === index && "active-tab"}`}
            onClick={() => setActiveTab(index)}
          >
            {tab.title}
            <div
              className={`tab-indicator ${
                activeTab === index && "tab-active-indicator"
              }`}
            ></div>
          </div>
        </div>
      ))}
    </div>
  );
};

export default Tabs;
