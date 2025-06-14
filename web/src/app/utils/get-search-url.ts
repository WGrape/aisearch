export const getSearchUrl = (conversation_id: number = 0, query: string = "", mode: string = "", search_uuid: string = "") => {
  // const prefix =
  //   process.env.NODE_ENV === "production" ? "/search.html" : "/search";
  const prefix = "/pages/search"
  search_uuid = "0" // 先不要使用rid, 暂无使用场景
  return `${prefix}?q=${encodeURIComponent(query)}&conversation_id=${conversation_id}&mode=${mode}&rid=${search_uuid}`;
};
