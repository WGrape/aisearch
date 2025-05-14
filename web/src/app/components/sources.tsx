import { Skeleton } from "@/app/components/skeleton";
import { Wrapper } from "@/app/components/wrapper";
import { Source } from "@/app/interfaces/source";
import { BookText } from "lucide-react";
import { FC } from "react";
import {Relate} from "@/app/interfaces/relate";

function getHostname(url: string): string {
  if (url.indexOf("http://") === 0) {
    url = url.substring(7); // 移除 "http://"
  } else if (url.indexOf("https://") === 0) {
      url = url.substring(8); // 移除 "https://"
  }
  return url.split("/")[0].split(":")[0]; // 取 hostname，去掉端口
}

const SourceItem: FC<{ source: Source; index: number }> = ({
  source,
  index,
}) => {
  const { id, name, url, snippet} = source;
  const domain = getHostname(url || "");
  return (
    <div
      className="relative text-xs py-3 px-3 bg-zinc-100 hover:bg-zinc-200 rounded-lg flex flex-col gap-2"
      key={id}
    >
      <a href={url} target="_blank" className="absolute inset-0"></a>
      <div className="font-medium text-zinc-950 text-ellipsis overflow-hidden whitespace-nowrap break-words">
          <div className="text-ellipsis whitespace-nowrap break-all text-zinc-400 overflow-hidden w-full" >
            {index + 1} - {domain}
          </div>
         <div className="flex-none flex items-center" style={{display: "inline-block", float: "right", marginTop: "-15px"}}>
              <img
                className="h-3 w-3"
                alt={domain}
                src={`https://www.google.com/s2/favicons?domain=${domain}&sz=${16}`}
              />
          </div>
        <div style={{color: "#555", marginTop: "10px"}}>{name ? name : "无法获取内容"}</div>
      </div>
      <div className="flex gap-2 items-center">
        <div className="flex-1 overflow-hidden">
          <div className="text-ellipsis break-all overflow-hidden" style={{maxHeight: "80px", color: "#888"}}>
            {snippet ? "简介："+snippet : ""}
          </div>
        </div>
      </div>
    </div>
  );
};

export const Sources: FC<{ relates: Relate[] | null; sources: Source[] }> = ({ relates, sources }) => {
  // 通过relates是否为空(请求完成后, relates必不为空, 如果没有推荐问题, 也会有默认数据), 判断是否请求完成, 如果请求完成了, sources为空就说明真的暂无参考, 否则只是表示正在加载中
  return (
    <Wrapper
      title={
        <>
          <BookText></BookText> Sources
        </>
      }
      content={
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-2">
          {sources.length > 0 ? (
            sources.map((item, index) => (
              <SourceItem
                key={item.id}
                index={index}
                source={item}
              ></SourceItem>
            ))
          ) : (relates === null || relates.length === 0) ? (
            // relates为空时显示加载中的样式
            <>
              <Skeleton className="max-w-sm h-16 bg-zinc-200/80"></Skeleton>
              <Skeleton className="max-w-sm h-16 bg-zinc-200/80"></Skeleton>
              <Skeleton className="max-w-sm h-16 bg-zinc-200/80"></Skeleton>
              <Skeleton className="max-w-sm h-16 bg-zinc-200/80"></Skeleton>
            </>
          ) : (
            // relates不为空时显示“暂无参考”
            <div className="text-left text-gray-500">暂无参考</div>
          )}
        </div>
      }
    ></Wrapper>
  );
};
