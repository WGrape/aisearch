"use client";
import { getSearchUrl } from "@/app/utils/get-search-url";
import { ArrowRight } from "lucide-react";
import { nanoid } from "nanoid";
import { useRouter } from "next/navigation";
import React, { FC, useState } from "react";

interface SearchProps {
  mode?: string; // 搜索模式
  shouldNavigate?: boolean; // 是否跳转到新页面
  onSearch?: (query: string, mode: string, rid: string) => void; // 自定义搜索逻辑回调
}

export const Search: FC<SearchProps> = ({ mode="simple", shouldNavigate = true, onSearch }) => {
  const [value, setValue] = useState("");
  const router = useRouter();
  return (
    // <form
    //   onSubmit={(e) => {
    //     e.preventDefault();
    //     if (value) {
    //       setValue("");
    //       router.push(getSearchUrl(encodeURIComponent(value), nanoid()));
    //     }
    //   }}
    // >
    <form
      onSubmit={(e) => {
        e.preventDefault();
        if (value) {
          const rid = nanoid();
          if (shouldNavigate) {
            localStorage.setItem("conversation_id", "0");
          }
          if (onSearch) {
            // 如果提供了 `onSearch` 回调，则调用它
            onSearch(value, mode, rid);
          } else if (shouldNavigate) {
            // 默认行为：跳转到新页面
            setValue("");
            router.push(getSearchUrl(0,value, mode, rid));
          }
          setValue("");
        }
      }}
    >
      <label
        className="relative bg-white flex items-center justify-center border ring-8 ring-zinc-300/20 py-2 px-2 rounded-lg gap-2 focus-within:border-zinc-300"
        htmlFor="search-bar"
      >
        <input
          id="search-bar"
          value={value}
          onChange={(e) => setValue(e.target.value)}
          autoFocus
          placeholder="请提出你的任何问题 ..."
          className="px-2 pr-6 w-full rounded-md flex-1 outline-none bg-white"
        />
        <button
          type="submit"
          className="w-auto py-1 px-2 bg-black border-black text-white fill-white active:scale-95 border overflow-hidden relative rounded-xl"
        >
          <ArrowRight size={16} />
        </button>
      </label>
    </form>
  );
};
