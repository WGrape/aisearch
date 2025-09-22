import os
import sys
import json
from openai import OpenAI
from web_search import search_web_tool, OPENAI_API_KEY, OPENAI_BASE_URL, WEBSEARCH_TOOL_DEFINITION

sys.path.append(os.path.dirname(os.path.abspath(__file__)))


