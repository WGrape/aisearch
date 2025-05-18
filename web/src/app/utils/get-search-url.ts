export const getSearchUrl = (conversation_id: number = 0, query: string = "", mode: string = "", search_uuid: string = "") => {
  const prefix =
    process.env.NODE_ENV === "production" ? "/search.html" : "/search";
  return `${prefix}?q=${encodeURIComponent(query)}&conversation_id=${conversation_id}&mode=${mode}&rid=${search_uuid}`;
};
