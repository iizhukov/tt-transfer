import "./news.scss";
import Post from "../post/Post";
import TextArea from "../textArea/TextArea";
import Button from "../ui/button/Button";

const News = () => {
  return (
    <div className="news-wrapper">
      <TextArea />
      <Button
        text="Отправить"
        height={40}
        width={160}
        style={{ fontWeight: 300, marginTop: 22, fontSize: 14 }}
      />
      <Post />
      <Post />
      <Post />
      <Post />
    </div>
  );
};

export default News;
