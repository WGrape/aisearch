"use client";
import { getSearchUrl } from "@/app/utils/get-search-url";
import { RefreshCcw } from "lucide-react";
import { nanoid } from "nanoid";
import { useRouter } from "next/navigation";

export const Title = ({ query, mode }: { query: string, mode: string }) => {
  const router = useRouter();
  return (
    // <div className="flex items-center pb-4 mb-6 border-b gap-4" style={{marginBottom: "10px"}}>
    <div className="flex items-center pb-4 border-b gap-4" style={{marginTop: "10px"}}>
      <div
        className="flex-1 text-lg sm:text-xl text-black text-ellipsis overflow-hidden whitespace-nowrap"
        title={query}
      >
        提问：{query}
      </div>
      <div className="flex-none">
        <button
          onClick={() => {
            // router.push(getSearchUrl(encodeURIComponent(query), nanoid()));
            router.push(getSearchUrl(0, query, mode, nanoid()));
          }}
          type="button"
          className="rounded flex gap-2 items-center bg-transparent px-2 py-1 text-xs font-semibold text-blue-500 hover:bg-zinc-100"
        >
          <RefreshCcw size={12}></RefreshCcw>Rewrite
        </button>
      </div>
    </div>
  );
};
