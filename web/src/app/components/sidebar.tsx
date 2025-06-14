"use client";
import React, { useEffect, useState, useRef } from "react";
import Link from "next/link";

type Session = {
  id: string;
  query: string;
  create_time: string;
  update_time: string;
};

export function Sidebar() {
  const [sessions, setSessions] = useState<Session[]>([]); // 定义类型为 Session 数组
  const [offset, setOffset] = useState(1); // 当前偏移量
  const [hasMore, setHasMore] = useState(true); // 是否还有更多数据
  const [loading, setLoading] = useState(false); // 加载状态
  const sidebarRef = useRef<HTMLDivElement>(null); // Sidebar 的引用

  const limit = 10; // 每页加载数量
  let isFetching = false; // 防止重复调用

  // 加载会话列表
  // 使用 useRef 存储最新的 offset
  // 由于 offset 的更新在 React 中是异步的，我们可以使用一个 useRef 来始终存储最新的 offset 值，并在请求中使用它：
  const offsetRef = useRef(1); // 使用 useRef 存储最新的 offset 值
  const fetchSessions = async () => {
    if (loading || !hasMore || isFetching) return;

    isFetching = true; // 防止重复调用
    setLoading(true);

    try {
      const response = await fetch(
        `http://127.0.0.1:8100/api/search/history/list?pg=${offsetRef.current}&pz=${limit}` // 使用 Ref 中存储的最新 offset
      );
      const result = await response.json();

      setSessions((prev) => [...prev, ...result.data.list]); // 合并新数据到旧数据
      setHasMore(result.data.list.length >= limit); // 更新是否还有更多数据

      // 更新 Ref 中的 offset
      offsetRef.current += 1; // 手动更新最新的 offset 值
    } catch (error) {
      console.error("Failed to fetch sessions:", error);
    } finally {
      setLoading(false);
      isFetching = false; // 请求完成后重置标志
    }
  };

  // 监听滚动事件
  const handleScroll = () => {
    if (!sidebarRef.current) return;

    const { scrollTop, scrollHeight, clientHeight } = sidebarRef.current;
    if (scrollTop + clientHeight >= scrollHeight - 10) {
      fetchSessions(); // 滚动到底部时加载更多数据
    }
  };

  // 删除会话
  const deleteSession = async (id: string) => {
    try {
      const response = await fetch(
        `http://127.0.0.1:8100/api/search/history/delete`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ id }), // 将 id 作为请求体参数传递
        }
      );

      if (response.ok) {
        setSessions((prev) =>
          prev.filter((session) => session.id !== id)
        ); // 从会话列表中移除已删除的会话
      } else {
        console.error("Failed to delete session");
      }
    } catch (error) {
      console.error("Error deleting session:", error);
    }
  };

  useEffect(() => {
    fetchSessions(); // 初次加载数据
  }, []); // 只在组件首次挂载时加载数据

  useEffect(() => {
    const sidebarElement = sidebarRef.current;
    if (sidebarElement) {
      sidebarElement.addEventListener("scroll", handleScroll);
    }
    return () => {
      if (sidebarElement) {
        sidebarElement.removeEventListener("scroll", handleScroll);
      }
    };
  }, []); // 监听滚动事件，不依赖其他状态

  return (
    <div
      ref={sidebarRef}
      className="fixed left-0 top-0 bottom-0 w-64 bg-gray-100 border-r border-gray-300 overflow-auto"
    >
      <h2 className="text-lg text-center p-4 border-b border-gray-300">
        <Link href="/" className="text-blue-500 hover:underline">
          Wgrape AISearch
        </Link>
      </h2>

      <ul className="p-4 space-y-2">
        {sessions.map((session, index) => (
          <li
            key={session.id}
            className="p-2 bg-white rounded shadow hover:bg-gray-200"
          >
            <Link href={`/conversation/${session.id}`} className="block">
              <div>{session.query}</div>
              <div className="flex items-center justify-between text-sm text-gray-500 mt-2">
                {/* 时间 */}
                <div className="text-right">
                  {new Date(session.create_time).toLocaleString()}
                </div>
                {/* 删除按钮 */}
                <button
                  className="text-red-500 bg-gray-100 p-1 rounded hover:bg-red-100"
                  onClick={(e) => {
                    e.preventDefault(); // 防止点击删除时触发跳转
                    const confirmDelete = window.confirm("确定要删除这个会话吗？"); // 弹窗确认
                    if (confirmDelete) {
                      deleteSession(session.id);
                    }
                  }}
                >
                  删除
                </button>
              </div>
              <div className="text-left text-xs text-gray-500">
                会话ID={session.id}
              </div>
            </Link>
          </li>
        ))}
      </ul>
      {loading && (
        <div className="text-center p-4 text-gray-500">加载中...</div>
      )}
      {!hasMore && (
        <div className="text-center p-4 text-gray-500">没有更多数据了</div>
      )}
    </div>
  );
}
