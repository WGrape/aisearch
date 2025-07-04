"use client";
import { Thought } from "@/app/components/thought";
import { Answer } from "@/app/components/answer";
import { Relates } from "@/app/components/relates";
import { Sources } from "@/app/components/sources";
import { Relate } from "@/app/interfaces/relate";
import { Source } from "@/app/interfaces/source";
// import { parseStreaming } from "@/app/utils/parse-streaming";
import { parseSSE } from "@/app/utils/parse-sse";
import { Annoyed } from "lucide-react";
import { FC, useEffect, useState } from "react";

export const Result: FC<{ conversation_id: number, query: string; mode: string; rid: string }> = ({ conversation_id, query, mode, rid }) => {
  const [thought, setThought] = useState<string>("");
  const [sources, setSources] = useState<Source[]>([]);
  const [markdown, setMarkdown] = useState<string>("");
  const [relates, setRelates] = useState<Relate[] | null>(null);
  const [error, setError] = useState<number | null>(null);
  useEffect(() => {
    const controller = new AbortController();
    void parseSSE(
      controller,
      conversation_id,
      mode,
      query,
      setThought,
      setSources,
      setMarkdown,
      setRelates,
      setError,
    );
    return () => {
      controller.abort();
    };
  }, [conversation_id, mode, query]);
  return (
    <div className="flex flex-col gap-8">
      <Thought thought={thought}></Thought>
      <Answer markdown={markdown} sources={sources}></Answer>
      <Sources relates={relates} sources={sources}></Sources>
      <Relates relates={relates}></Relates>
      {error && (
        <div className="absolute inset-4 flex items-center justify-center bg-white/40 backdrop-blur-sm">
          <div className="p-4 bg-white shadow-2xl rounded text-blue-500 font-medium flex gap-4">
            <Annoyed></Annoyed>
            {error === 429
              ? "Sorry, you have made too many requests recently, try again later."
              : "Sorry, we might be overloaded, try again later."}
          </div>
        </div>
      )}
    </div>
  );
};