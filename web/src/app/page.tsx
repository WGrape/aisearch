"use client";
import { Footer } from "@/app/components/footer";
import { Logo } from "@/app/components/logo";
import { PresetQuery } from "@/app/components/preset-query";
import { Search } from "@/app/components/search";
import { Sidebar } from "@/app/components/sidebar"; // 引入 Sidebar
import { nanoid } from "nanoid";
import React, { useState } from "react";

// 首页
export default function Home() {
  const rid1 = nanoid() + "-1"; // 在服务器端生成随机值
  const rid2 = nanoid() + "-2"; // 在服务器端生成随机值
  console.log("rid1: " + rid1, "----", "rid2: " + rid2);

  // 使用 useState 管理 mode 状态
  const [mode, setMode] = useState("simple");

  return (
    <div className="absolute inset-0 min-h-[500px] flex items-center justify-center">
      <Sidebar /> {/* 左侧固定栏 */}
      <div className="relative flex flex-col gap-8 px-4 -mt-24">
        <Logo></Logo>

        {/* 搜索组件 */}
        <Search mode={mode} shouldNavigate={true}></Search>

        {/* 模式切换选项 */}
        <div className="flex gap-4 justify-center">
          <button
            className={`px-2 py-2 rounded-lg text-sm ${
              mode === "simple" ? "bg-blue-500 text-white" : "bg-gray-200 text-black"
            }`}
            onClick={() => setMode("simple")}
          >
            普通模式
          </button>
          <button
            className={`px-2 py-2 rounded-lg text-sm ${
              mode === "professional" ? "bg-blue-500 text-white" : "bg-gray-200 text-black"
            }`}
            onClick={() => setMode("professional")}
          >
            专业模式
          </button>
        </div>

        {/* 预设查询 */}
        <div className="flex gap-2 flex-wrap justify-center">
          <PresetQuery query="请给我推荐最新的新闻" mode={mode} rid={rid1}></PresetQuery>
          <PresetQuery query="如何更好的学习Python语言" mode={mode} rid={rid2}></PresetQuery>
        </div>

        <Footer></Footer>
      </div>
    </div>
  );
}