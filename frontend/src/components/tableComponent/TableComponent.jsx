import "./tableComponent.scss";

const TableComponent = ({ headers, body }) => {
  return (
    <div className={"table-wrap"}>
      <table className="table-component">
        <thead>
          <tr>
            {headers.map((header) => (
              <td>{header}</td>
            ))}
          </tr>
        </thead>
        <tbody>
          {body.map((item) => {
            return (
              <tr
                className={`${item.items.includes("Выполнен") && "green"} ${
                  item.items.includes("Срочно") && "red"
                }`}
              >
                {item.items.map((title) => (
                  <td>{title}</td>
                ))}
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
};

export default TableComponent;
