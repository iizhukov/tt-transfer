import "./blockHeader.scss";
import Button from "../ui/button/Button";
import searchIcon from "../../assets/find.svg";
import filterIcon from "../../assets/smart-filter.svg";
import excel from "../../assets/excel.svg";

const BlockHeader = () => {
  return (
    <div className="header-block-wrap">
      <div className={"left-wrap"}>
        <div className={"header-block-input-wrap"}>
          <form action="">
            <input
              type="text"
              className="header-block-input"
              placeholder={"Поиск"}
            />
          </form>
          <img src={searchIcon} alt="" className="search-icon" />
        </div>
        <div className="smart-filter">
          <div className="smart-filter-columns">
            <img src={filterIcon} alt="" />
            <div>Умный фильтр</div>
          </div>
        </div>
      </div>
      <div className={"left-wrap"}>
        <div className="excel-upload">
          <div className="smart-filter-columns">
            <img src={excel} alt="" />
            <div>Выгрузить в Excel</div>
          </div>
        </div>
        <Button text="Добавить заказ" height={45} width={180} />
      </div>
    </div>
  );
};

export default BlockHeader;
