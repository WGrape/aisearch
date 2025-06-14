"use client";
import { Result } from "@/app/components/result";
import { Search } from "@/app/components/search";
import { Title } from "@/app/components/title";
import { Sidebar } from "@/app/components/sidebar";
import { Suspense, useEffect, useState } from "react";
import { useSearchParams } from "next/navigation";

export default function SearchPage() {
  const [searchRecords, setSearchRecords] = useState<
    { query: string; mode: string; rid: string; conversation_id: number }[]
  >([]);
  const searchParams = useSearchParams();

  // Handle initial search from URL parameters
  useEffect(() => {
    const query = searchParams.get("q") ? decodeURIComponent(searchParams.get("q")!) : "";
    const mode = searchParams.get("mode") || "simple";
    const rid = searchParams.get("rid");

    const local_conversation_id = localStorage.getItem("conversation_id");
    const parsedId = local_conversation_id === null ? 0 : parseInt(local_conversation_id, 10);

    if (query && rid) {
      setSearchRecords([{ query, mode, rid, conversation_id: parsedId }]);
    }
  }, [searchParams]); // Ensure this effect only runs when `searchParams`

  const handleSearch = (query: string, mode: string, rid: string) => {
    const local_conversation_id = localStorage.getItem("conversation_id");
    const parsedId = local_conversation_id === null ? 0 : parseInt(local_conversation_id, 10);
    if (parsedId) {
      setSearchRecords((prev) => {
        // 如果不是首次搜索，保留之前的记录
        return [...prev, { query, mode, rid, conversation_id: parsedId }];
      });
    } else {
      console.error("No conversation_id found in localStorage.");
    }
  };

  return (
    <div className="absolute inset-0 bg-[url('/bg.svg')]">
      <Sidebar />
      <div className="mx-auto max-w-3xl absolute inset-4 md:inset-8 bg-white">
        <div className="h-20 pointer-events-none rounded-t-2xl w-full backdrop-filter absolute top-0 bg-gradient-to-t from-transparent to-white [mask-image:linear-gradient(to_bottom,white,transparent)]"></div>
        <div className="px-4 md:px-8 pt-6 pb-24 rounded-2xl ring-8 ring-zinc-300/20 border border-zinc-200 h-full overflow-auto">
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