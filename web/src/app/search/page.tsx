"use client";
import { Result } from "@/app/components/result";
import { Search } from "@/app/components/search";
import { Title } from "@/app/components/title";
import { Sidebar } from "@/app/components/sidebar"; // 引入 Sidebar
import { useState } from "react";
import { Suspense } from "react";

// 搜索结果页面
export default function SearchPage() {
  const [searchRecords, setSearchRecords] = useState<{ query: string; mode: string; rid: string }[]>([]); // 搜索记录

  // 处理搜索逻辑
  const handleSearch = (query: string, mode: string, rid: string) => {
    setSearchRecords((prev) => [...prev, { query, mode, rid }]); // 新增搜索记录
  };

  return (
    <div className="absolute inset-0 bg-[url('/bg.svg')]">
      <Sidebar /> {/* 左侧固定栏 */}
      <div className="mx-auto max-w-3xl absolute inset-4 md:inset-8 bg-white">
        <div className="h-20 pointer-events-none rounded-t-2xl w-full backdrop-filter absolute top-0 bg-gradient-to-t from-transparent to-white [mask-image:linear-gradient(to_bottom,white,transparent)]"></div>
        <div className="px-4 md:px-8 pt-6 pb-24 rounded-2xl ring-8 ring-zinc-300/20 border border-zinc-200 h-full overflow-auto">
          {/* 渲染所有搜索记录 */}
          {searchRecords.map((record, index) => (
            <div key={`${record.rid}-${index}`} className="mb-8">
              <Title query={record.query} mode={record.mode}></Title>
              <Result key={record.rid} conversation_id={0} query={record.query} rid={record.rid} mode={record.mode}></Result>
            </div>
          ))}
        </div>
        <div className="h-80 pointer-events-none w-full rounded-b-2xl backdrop-filter absolute bottom-0 bg-gradient-to-b from-transparent to-white [mask-image:linear-gradient(to_top,white,transparent)]"></div>
        <div className="absolute z-10 flex items-center justify-center bottom-6 px-4 md:px-8 w-full">
          <div className="w-full">
            <Suspense>
              <Search shouldNavigate={false} onSearch={handleSearch} /> {/* 使用自定义搜索逻辑 */}
            </Suspense>
          </div>
        </div>
      </div>
    </div>
  );
}
