"use client";

import React, { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import {Relate} from "@/app/interfaces/relate";
import { Sidebar } from "@/app/components/sidebar"; // 引入 Sidebar
import { Title } from "@/app/components/title"; // 复用搜索页面的标题组件
import { Thought } from "@/app/components/thought"; // 引入 Thought 组件
import { Answer } from "@/app/components/answer"; // 引入 Answer 组件
import { Sources } from "@/app/components/sources"; // 引入 Sources 组件
import { Search } from "@/app/components/search"; // 复用搜索组件
import { Suspense } from "react";
import { Annoyed } from "lucide-react";

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

export default function SessionDetails() {
    const params = useParams(); // 从 URL 动态路由中获取参数
  const id = params?.id; // 获取动态参数 `id`
  const [sessionDetails, setSessionDetails] = useState<SessionDetailItem[]>([]); // 会话详情列表
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<number | null>(null);
  const [countdown, setCountdown] = useState(5); // 倒计时初始值为 5 秒

  useEffect(() => {
    if (!id) return; // 如果没有 `id`，不进行请求

    const fetchSessionDetails = async () => {
      setLoading(true);
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
      } catch (error) {
        console.error("Failed to fetch session details:", error);
        setError(500); // 假设错误状态码为 500
      } finally {
        setLoading(false);
      }
    };

    fetchSessionDetails();
  }, [id]);

  // 倒计时逻辑
  useEffect(() => {
    if (!sessionDetails || sessionDetails.length === 0) {
      const timer = setInterval(() => {
        setCountdown((prev) => {
          if (prev === 1) {
            clearInterval(timer); // 倒计时结束时清除定时器
            window.location.href = '/'; // 跳转到首页
          }
          return prev - 1;
        });
      }, 1000);

      return () => clearInterval(timer); // 清除定时器以防止内存泄漏
    }
  }, [sessionDetails]);

  // 加载中状态
  if (loading) {
    return <div className="text-center p-4 text-gray-500">加载中...</div>;
  }

  // 错误状态
  if (error) {
    return (
      <div className="absolute inset-4 flex items-center justify-center bg-white/40 backdrop-blur-sm">
        <div className="p-4 bg-white shadow-2xl rounded text-blue-500 font-medium flex gap-4">
          <Annoyed></Annoyed>
          {error === 429
            ? "Sorry, you have made too many requests recently, try again later."
            : "Sorry, we might be overloaded, try again later."}
        </div>
      </div>
    );
  }

  // 未找到会话详情
  const isEmpty = !sessionDetails || sessionDetails.length === 0;
  return (
    <div className="absolute inset-0 bg-[url('/bg.svg')]">
      <Sidebar /> {/* 左侧固定栏 */}
      {isEmpty ? (
        <div className="text-center p-4 text-gray-500" style={{ position: "absolute", left: "50%", top: "50%" }}>
          未找到会话详情 | 会话ID={id}
          <span className="block text-sm text-gray-400">
            {countdown} 秒后将自动跳转到首页...
          </span>
        </div>
      ) : (
        <div className="mx-auto max-w-3xl absolute inset-4 md:inset-8 bg-white">
          <div className="h-20 pointer-events-none rounded-t-2xl w-full backdrop-filter absolute top-0 bg-gradient-to-t from-transparent to-white [mask-image:linear-gradient(to_bottom,white,transparent)]"></div>
          <div className="px-4 md:px-8 pt-6 pb-24 rounded-2xl ring-8 ring-zinc-300/20 border border-zinc-200 h-full overflow-auto">
            <div className="space-y-6">
              {sessionDetails.map((item) => (
                <div key={item.message_id} className="flex flex-col gap-8">
                  <Title query={item.query}></Title>
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
                </div>
              ))}
            </div>
          </div>
          <div className="h-80 pointer-events-none w-full rounded-b-2xl backdrop-filter absolute bottom-0 bg-gradient-to-b from-transparent to-white [mask-image:linear-gradient(to_top,white,transparent)]"></div>
          <div className="absolute z-10 flex items-center justify-center bottom-6 px-4 md:px-8 w-full">
            <div className="w-full">
              <Suspense>
                <Search />
              </Suspense>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}