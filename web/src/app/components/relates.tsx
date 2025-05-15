import { PresetQuery } from "@/app/components/preset-query";
import { Skeleton } from "@/app/components/skeleton";
import { Wrapper } from "@/app/components/wrapper";
import { Relate } from "@/app/interfaces/relate";
import { MessageSquareQuote } from "lucide-react";
import React, { FC } from "react";
import { nanoid } from "nanoid";

export const Relates: FC<{ relates: Relate[] | null }> = ({ relates }) => {
  const rid = nanoid(); // 在服务器端生成随机值

  return (
    <Wrapper
      title={
        <>
          <MessageSquareQuote></MessageSquareQuote> Related
        </>
      }
      content={
        <div className="flex gap-2 flex-col">
          {relates !== null ? (
            relates.length > 0 ? (
              relates.map(({ question }) => (
                <PresetQuery key={question} query={question} rid={rid}></PresetQuery>
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
