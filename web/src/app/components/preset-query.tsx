import { getSearchUrl } from "@/app/utils/get-search-url";
import { nanoid } from "nanoid";
import Link from "next/link";
import React, { FC, useMemo } from "react";

export const PresetQuery: FC<{ query: string; rid: string }> = ({ query, rid}) => {
  // 会报错: Warning: Prop `href` did not match. Server: "xxx", Client: "xxx"
  // const rid = useMemo(() => nanoid(), [query]);
  // const rid = "fixed_rid" // 使用固定的rid可以解决, 最终方案是使用传来的rid参数

  return (
    <Link
      prefetch={false}
      title={query}
      href={getSearchUrl(0,query, rid)}
      className="border border-zinc-200/50 text-ellipsis overflow-hidden text-nowrap items-center rounded-lg bg-zinc-100 hover:bg-zinc-200/80 hover:text-zinc-950 px-2 py-1 text-xs font-medium text-zinc-600"
    >
      {query}
    </Link>
  );
};
