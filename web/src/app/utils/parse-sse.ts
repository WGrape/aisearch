import { Relate } from "@/app/interfaces/relate";
import { Source } from "@/app/interfaces/source";

const LLM_SPLIT = "__LLM_RESPONSE__";
const RELATED_SPLIT = "__RELATED_QUESTIONS__";

export const parseSSE = (
  controller: AbortController,
  query: string,
  mode: string = "simple",
  onThought: (value: string) => void,
  onSources: (value: Source[]) => void,
  onMarkdown: (value: string) => void,
  onRelates: (value: Relate[]) => void,
  onError?: (status: number) => void,
) => {
  const eventSource = new EventSource(`http://127.0.0.1:8100/api/search_sse?query=${encodeURIComponent(query)}&mode=${mode}`);

  var answer = ""

  eventSource.onmessage = (event) => {
    const sse_event_data = JSON.parse(event.data);
    const data = sse_event_data.data;
    console.log("onmessage: ", sse_event_data, data)
    if (sse_event_data.event == "message_end") {
      console.log("SSE connection closed: message_end")
      eventSource.close()

      const conversation_id = data.conversation_id; 
      fetch(`http://127.0.0.1:8100/api/search/predict_questions?conversation_id=${conversation_id}`)
      .then(response => {
          if (!response.ok) {
              throw new Error(`HTTP error! Status: ${response.status}`);
          }
          return response.json();
      })
      .then(result => {
        onRelates(result.data.questions);
          console.log("Predict Questions Response:", result);
      })
      .catch(error => {
          console.error("Error fetching predict_questions:", error);
      });

      return;
    }

    try {
      if (data.type === "ping"){
        return;
      }
      else if (data.type === "analyzer_result") {
        onThought(data.item.content || "")
      }
      else if (data.type === "reference") {
        onSources(data.item.list || [])
      }
      else if (data.type === "generation") {
        answer = answer + data.item.content
        onMarkdown(
          answer
            .replace(/\[\[([cC])itation/g, "[citation")
            .replace(/[cC]itation:(\d+)]]/g, "citation:$1]")
            .replace(/\[\[([cC]itation:\d+)]](?!])/g, `[$1]`)
            .replace(/\[[cC]itation:(\d+)]/g, "[citation]($1)")
        );
      }
    } catch (error) {
      console.error("Error parsing SSE data:", error);
    }
  };

  eventSource.onopen = () => {
    console.log("SSE connection established successfully.");
  };

  eventSource.onerror = (event) => {
    console.error("SSE connection error:", event);
    onError?.(500);
    eventSource.close();
  };

  controller.signal.addEventListener("abort", () => {
    eventSource.close();
  });
};
