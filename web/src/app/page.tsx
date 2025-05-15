// "use client"; 如果不移除, 还是报错 Warning: Prop `href` did not match.
import { Footer } from "@/app/components/footer";
import { Logo } from "@/app/components/logo";
import { PresetQuery } from "@/app/components/preset-query";
import { Search } from "@/app/components/search";
import { Sidebar } from "@/app/components/sidebar"; // 引入 Sidebar
import { nanoid } from "nanoid";
import React from "react";

export default function Home() {
  const rid1 = nanoid()+"-1"; // 在服务器端生成随机值
  const rid2 = nanoid()+"-2"; // 在服务器端生成随机值
  console.log("rid1: "+ rid1, "----", "rid2: "+ rid2)

  return (
    <div className="absolute inset-0 min-h-[500px] flex items-center justify-center">
      <Sidebar /> {/* 左侧固定栏 */}
      <div className="relative flex flex-col gap-8 px-4 -mt-24">
        <Logo></Logo>
        <Search></Search>
        <div className="flex gap-2 flex-wrap justify-center">
          <PresetQuery query="Who said live long and prosper?" rid={rid1}></PresetQuery>
          <PresetQuery query="Why do we only see one side of the moon?" rid={rid1}></PresetQuery>
        </div>
        <Footer></Footer>
      </div>
    </div>
  );
}
