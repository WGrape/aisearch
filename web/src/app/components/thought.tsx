import { PresetQuery } from "@/app/components/preset-query";
import { Skeleton } from "@/app/components/skeleton";
import { Wrapper } from "@/app/components/wrapper";
import { MessageSquareQuote } from "lucide-react";
import React, { FC } from "react";

export const Thought: FC<{ thought: string | null }> = ({ thought }) => {
  return (
    <Wrapper
      title={
        <>
          <MessageSquareQuote></MessageSquareQuote> Thought
        </>
      }
      content={
        <div className="flex gap-2 flex-col">
          {thought !== null ? (
            <div className="text-sm">{thought}</div>
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
