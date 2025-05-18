"use client";

import React, { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import { Sidebar } from "@/app/components/sidebar"; // 引入 Sidebar
import { Title } from "@/app/components/title"; // 复用搜索页面的标题组件
import { Answer } from "@/app/components/answer"; // 引入 Answer 组件
import { Sources } from "@/app/components/sources"; // 引入 Sources 组件
import { Search } from "@/app/components/search"; // 复用搜索组件
import { Suspense } from "react";
import { Result } from "@/app/components/result";
import {Relates} from "@/app/components/relates";

type SessionDetailItem = {
  answer: string;
  conversation_id: number;
  create_time: string;
  message_id: number;
  mode: string;
  query: string;
  references: string[];
  update_time: string;
};

// 详情页面
export default function SessionDetails() {
  const params = useParams();
  // const id = params?.id;
  const id = Array.isArray(params?.id) ? params.id[0] : params?.id || '';

  const [sessionDetails, setSessionDetails] = useState<SessionDetailItem[]>([]); // 初始会话详情
  const [searchRecords, setSearchRecords] = useState<{ query: string; mode: string; rid: string }[]>([]); // 搜索记录
  const [loading, setLoading] = useState(true); // 加载状态
  const [error, setError] = useState<string | null>(null); // 错误状态

  // 加载会话详情数据
  useEffect(() => {
    if (!id) return;

    const fetchSessionDetails = async () => {
      setLoading(true);
      setError(null);
      try {
        const response = await fetch(`http://127.0.0.1:8100/api/search/history/get?id=${id}`, {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
          },
        });

        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }

        const result = await response.json();
        setSessionDetails(result.data.list || []); // 假设返回的详情数据在 `data.list` 中
      } catch (err) {
        setError("加载会话详情失败，请稍后重试。");
        console.error("Failed to fetch session details:", err);
      } finally {
        setLoading(false);
      }
    };

    fetchSessionDetails();
  }, [id]);

  // 搜索逻辑：新增搜索记录
  const handleSearch = (query: string, mode: string, rid: string) => {
    setSearchRecords((prev) => [...prev, { query, mode, rid }]);
  };

  // 加载中状态
  if (loading) {
    return <div className="text-center p-4 text-gray-500">加载中...</div>;
  }

  // 错误状态
  if (error) {
    return (
      <div className="absolute inset-4 flex items-center justify-center bg-white/40 backdrop-blur-sm">
        <div className="p-4 bg-white shadow-2xl rounded text-red-500 font-medium">
          {error}
        </div>
      </div>
    );
  }

  return (
    <div className="absolute inset-0 bg-[url('/bg.svg')]">
      <Sidebar /> {/* 左侧固定栏 */}
      <div className="mx-auto max-w-3xl absolute inset-4 md:inset-8 bg-white">
        <div className="h-20 pointer-events-none rounded-t-2xl w-full backdrop-filter absolute top-0 bg-gradient-to-t from-transparent to-white [mask-image:linear-gradient(to_bottom,white,transparent)]"></div>
        <div className="px-4 md:px-8 pt-6 pb-24 rounded-2xl ring-8 ring-zinc-300/20 border border-zinc-200 h-full overflow-auto">
          {/* 渲染初始会话详情 */}
          {sessionDetails.map((item) => (
            <div key={item.message_id} className="flex flex-col gap-8" style={{marginBottom: "20px"}}>
              <div style={{marginBottom: "-30px"}}>
                <Title query={item.query} mode={item.mode}></Title>
              </div>
              <Answer
                markdown={item.answer}
                sources={item.references.map((ref, index) => ({
                  id: `source-${index}`,
                  name: ref,
                  url: ref,
                  isFamilyFriendly: true,
                  displayUrl: ref,
                  snippet: "",
                  deepLinks: [],
                  dateLastCrawled: new Date().toISOString(),
                  cachedPageUrl: "",
                  language: "en",
                  isNavigational: false,
                }))}
              />
              <Sources
                relates={[{ question: "推荐问题" }]}
                sources={item.references.map((ref, index) => ({
                  id: `source-${index}`,
                  name: ref,
                  url: ref,
                  isFamilyFriendly: true,
                  displayUrl: ref,
                  snippet: "",
                  deepLinks: [],
                  dateLastCrawled: new Date().toISOString(),
                  cachedPageUrl: "",
                  language: "en",
                  isNavigational: false,
                }))}
              />
              {/*会话详情中是没有这个相关问题推荐的*/}
              {/*<Relates relates={relates}></Relates>*/}
            </div>
          ))}

          {/* 渲染后续搜索记录 */}
          {searchRecords.map((record, index) => (
            <div key={`${record.rid}-${index}`} className="mb-8">
              <Title query={record.query} mode={record.mode}></Title>
              <Result key={record.rid} conversation_id={parseInt(id,10)} query={record.query} mode={record.mode} rid={record.rid}></Result>
              {/* Sources 数据需要从 Result 组件中获取，或者由后端返回 */}
              {/* 如果需要 Sources，您可以在 Result 渲染完成后动态加载相关数据 */}
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
