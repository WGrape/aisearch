"use client";
import { Result } from "@/app/components/result";
import { Search } from "@/app/components/search";
import { Title } from "@/app/components/title";
import { Sidebar } from "@/app/components/sidebar";
import { Suspense, useState } from "react";

export default function SearchPage() {
  const [searchRecords, setSearchRecords] = useState<
    { query: string; mode: string; rid: string; conversation_id: number }[]
  >([]);

  // 自定义搜索逻辑
  const handleSearch = (query: string, mode: string, rid: string) => {
    const conversation_id = 0; // 如果需要动态生成，可以替换为实际逻辑
    setSearchRecords((prev) => [
      ...prev,
      { query, mode, rid, conversation_id },
    ]);
  };

  return (
    <div className="absolute inset-0 bg-[url('/bg.svg')]">
      <Sidebar />
      <div className="mx-auto max-w-3xl absolute inset-4 md:inset-8 bg-white">
        <div className="h-20 pointer-events-none rounded-t-2xl w-full backdrop-filter absolute top-0 bg-gradient-to-t from-transparent to-white [mask-image:linear-gradient(to_bottom,white,transparent)]"></div>
        <div className="px-4 md:px-8 pt-6 pb-24 rounded-2xl ring-8 ring-zinc-300/20 border border-zinc-200 h-full overflow-auto">
          {/* 渲染所有搜索记录 */}
          {searchRecords.map((record, index) => (
            <div key={`${record.rid}-${index}`} className="mb-8">
              <Title query={record.query} mode={record.mode}></Title>
              <Result
                conversation_id={record.conversation_id}
                query={record.query}
                mode={record.mode}
                rid={record.rid}
              ></Result>
            </div>
          ))}
        </div>
        <div className="h-80 pointer-events-none w-full rounded-b-2xl backdrop-filter absolute bottom-0 bg-gradient-to-b from-transparent to-white [mask-image:linear-gradient(to_top,white,transparent)]"></div>
        <div className="absolute z-10 flex items-center justify-center bottom-6 px-4 md:px-8 w-full">
          <div className="w-full">
            <Suspense>
              <Search shouldNavigate={false} onSearch={handleSearch} />
            </Suspense>
          </div>
        </div>
      </div>
    </div>
  );
}
