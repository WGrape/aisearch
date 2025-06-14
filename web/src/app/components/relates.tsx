import { Skeleton } from "@/app/components/skeleton";
import { Wrapper } from "@/app/components/wrapper";
import { Relate } from "@/app/interfaces/relate";
import { MessageSquareQuote } from "lucide-react";
import React, { FC } from "react";
import { nanoid } from "nanoid";

export const Relates: FC<{ relates: Relate[] | null }> = ({ relates }) => {
  const rid = nanoid(); // 在服务器端生成随机值

  const simulateTyping = (inputElement: HTMLInputElement, text: string, callback?: () => void) => {
  let index = 0;

  const typeCharacter = () => {
    if (index < text.length) {
      // 当前字符
      const currentChar = text[index];

      // 更新输入框的值
      inputElement.value += currentChar;

      // 触发 `input` 事件
      const inputEvent = new Event("input", { bubbles: true });
      inputElement.dispatchEvent(inputEvent);

      // 继续输入下一个字符
      index++;
      setTimeout(typeCharacter, 40); // 每个字符间隔 100ms
    } else {
      // 完成输入后调用回调函数
      if (callback) {
        callback();
      }
    }
  };

  // 开始模拟输入
  typeCharacter();
};

const handleRelateClick = (question: string) => {
  const inputElement = document.getElementById("search-bar") as HTMLInputElement;

  if (inputElement) {
    // 清空输入框
    inputElement.value = "";

    // 模拟逐字符输入
    simulateTyping(inputElement, question, () => {
      console.log("Typing completed!");

      // 可选：模拟按下回车键
      const keydownEvent = new KeyboardEvent("keydown", {
        key: "Enter",
        code: "Enter",
        keyCode: 13,
        bubbles: true,
      });
      inputElement.dispatchEvent(keydownEvent);
    });
  } else {
    console.error("Input element with id 'search-bar' not found.");
  }
};

  return (
    <Wrapper
      title={
        <>
          <MessageSquareQuote /> Related
        </>
      }
      content={
        <div className="gap-2 flex-col">
          {relates !== null ? (
            relates.length > 0 ? (
              relates.map(({ question }) => (
                <button
                  key={question}
                  onClick={() => handleRelateClick(question)}
                  // className="text-sm text-blue-500 hover:underline"
                  className="border border-zinc-200/50 text-ellipsis overflow-hidden text-nowrap items-center rounded-lg bg-zinc-100 hover:bg-zinc-200/80 hover:text-zinc-950 px-2 py-1 text-xs font-medium text-zinc-600"
                >
                  {question}
                </button>
              ))
            ) : (
              <div className="text-sm">No related questions.</div>
            )
          ) : (
            <>
              <Skeleton className="w-full h-5 bg-zinc-200/80"></Skeleton>
              <Skeleton className="w-full h-5 bg-zinc-200/80"></Skeleton>
              <Skeleton className="w-full h-5 bg-zinc-200/80"></Skeleton>
            </>
          )}
        </div>
      }
    ></Wrapper>
  );
};