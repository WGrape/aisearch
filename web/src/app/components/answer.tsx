import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/app/components/popover";
import { Skeleton } from "@/app/components/skeleton";
import { Wrapper } from "@/app/components/wrapper";
import { Source } from "@/app/interfaces/source";
import { BookOpenText } from "lucide-react";
import { FC } from "react";
import Markdown from "react-markdown";
import React from "react";

type CustomTextRendererProps = {
  children: React.ReactNode; // ReactMarkdown 的子节点类型
};

function CustomTextRenderer({ children }: CustomTextRendererProps) {
  // 将 children 转换为字符串或 React 元素数组
  const renderChildren = (child: React.ReactNode): React.ReactNode => {
    if (typeof child === "string") {
      // 对字符串进行处理
      const parts = child.split(/(\[citation:\d+\])/g);

      return parts.map((part, index) => {
        if (part.match(/\[citation:(\d+)\]/)) {
          const citationNumber = part.match(/\[citation:(\d+)\]/)?.[1];
          return (
            <sup
              key={`citation-${index}`}
              style={{
                display: "inline-flex",
                alignItems: "center",
                justifyContent: "center",
                width: "1.5em",
                height: "1.5em",
                marginLeft: "0.2em",
                fontSize: "0.8em",
                backgroundColor: "#ddd", // 灰色背景
                color: "black", // 字体颜色
                borderRadius: "50%", // 圆形效果
                fontWeight: "bold", // 字体加粗
                lineHeight: "1.5em", // 垂直居中
              }}
            >
              {citationNumber}
            </sup>
          );
        } else {
          return part;
        }
      });
    } else {
      // 如果是 React 元素，直接返回
      return child;
    }
  };

  return <>{React.Children.map(children, renderChildren)}</>;
}

export const Answer: FC<{ markdown: string; sources: Source[] }> = ({
  markdown,
  sources,
}) => {
  return (
    <Wrapper
      title={
        <>
          <BookOpenText></BookOpenText> Answer
        </>
      }
      content={
        markdown ? (
          <div className="prose prose-sm max-w-full">
            <Markdown
              components={{
                // Customize the rendering of text nodes
                p: ({ children }) => <p><CustomTextRenderer>{children}</CustomTextRenderer></p>, // 小心这里的处理会影响加粗等P标签内可能存在的样式，所以需要兼容
                a: ({ node: _, ...props }) => {
                  if (!props.href) return <></>;
                  const source = sources[+props.href - 1];
                  if (!source) return <></>;
                  return (
                    <span className="inline-block w-4">
                      <Popover>
                        <PopoverTrigger asChild>
                          <span
                            title={source.name}
                            className="inline-block cursor-pointer transform scale-[60%] no-underline font-medium bg-zinc-300 hover:bg-zinc-400 w-6 text-center h-6 rounded-full origin-top-left"
                          >
                            {props.href}
                          </span>
                        </PopoverTrigger>
                        <PopoverContent
                          align={"start"}
                          className="max-w-screen-md flex flex-col gap-2 bg-white shadow-transparent ring-zinc-50 ring-4 text-xs"
                        >
                          <div className="text-ellipsis overflow-hidden whitespace-nowrap font-medium">
                            {source.name}
                          </div>
                          <div className="flex gap-4">
                            {source.primaryImageOfPage?.thumbnailUrl && (
                              <div className="flex-none">
                                <img
                                  className="rounded h-16 w-16"
                                  width={source.primaryImageOfPage?.width}
                                  height={source.primaryImageOfPage?.height}
                                  src={source.primaryImageOfPage?.thumbnailUrl}
                                />
                              </div>
                            )}
                            <div className="flex-1">
                              <div className="line-clamp-4 text-zinc-500 break-words">
                                {source.snippet}
                              </div>
                            </div>
                          </div>

                          <div className="flex gap-2 items-center">
                            <div className="flex-1 overflow-hidden">
                              <div className="text-ellipsis text-blue-500 overflow-hidden whitespace-nowrap">
                                <a
                                  title={source.name}
                                  href={source.url}
                                  target="_blank"
                                >
                                  {source.url}
                                </a>
                              </div>
                            </div>
                            <div className="flex-none flex items-center relative">
                              <img
                                className="h-3 w-3"
                                alt={source.url}
                                src={`https://www.google.com/s2/favicons?domain=${source.url}&sz=${16}`}
                              />
                            </div>
                          </div>
                        </PopoverContent>
                      </Popover>
                    </span>
                  );
                },
              }}
            >
              {markdown}
            </Markdown>
          </div>
        ) : (
          <div className="flex flex-col gap-2">
            <Skeleton className="max-w-sm h-4 bg-zinc-200"></Skeleton>
            <Skeleton className="max-w-lg h-4 bg-zinc-200"></Skeleton>
            <Skeleton className="max-w-2xl h-4 bg-zinc-200"></Skeleton>
            <Skeleton className="max-w-lg h-4 bg-zinc-200"></Skeleton>
            <Skeleton className="max-w-xl h-4 bg-zinc-200"></Skeleton>
          </div>
        )
      }
    ></Wrapper>
  );
};
