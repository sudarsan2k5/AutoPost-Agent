from langchain.agents import tool
from tools import call_linkedin, call_twitter
from langchain_openai import ChatOpenAI
from config import OPENAI_API_KEY
from langgraph.prebuilt import create_react_agent

@tool
def post_to_linkedin(topic: str) -> str:
    """
    Generate and post engaging content to LinkedIn about a specific topic.
    Use this when the user wants to create and share a LinkedIn post.
    The topic should be extracted from the user's request.
    
    Args:
        topic: The main subject or theme for the LinkedIn post
        
    Returns:
        Success message with the generated content
    """
    return call_linkedin(topic)

@tool
def post_to_twitter(topic: str) -> str:
    """
    Generate and post engaging content to Twitter about a specific topic.
    Use this when the user wants to create and share a Twitter post.
    The topic should be extracted from the user's request.
    
    Args:
        topic: The main subject or theme for the Twitter post
        
    Returns:
        Success message with the generated content
    """
    return call_twitter(topic)

llm = ChatOpenAI(
    model="gpt-4",
    temperature=0.2,
    api_key=OPENAI_API_KEY
)

tools = [
    post_to_linkedin,
    post_to_twitter,
]

graph = create_react_agent(
    llm,
    tools=tools
)

SYSTEM_PROMPT = """
You are a Social Media AI Assistant that helps users create and share engaging content on social media platforms.
You have access to two main tools:

1. `post_to_linkedin`: Use this tool when the user wants to create and post content to LinkedIn. Extract the topic from their request.
2. `post_to_twitter`: Use this tool when the user wants to create and post content to Twitter. Extract the topic from their request.

Examples of user requests:
- "Write an interesting post about AI and post to LinkedIn" → Use post_to_linkedin with topic "AI"
- "Create a Twitter post about productivity tips" → Use post_to_twitter with topic "productivity tips"
- "Post about climate change on LinkedIn" → Use post_to_linkedin with topic "climate change"

Always extract the main topic from the user's request and use the appropriate tool. Be helpful and confirm what you're doing.
"""

def parse_response(stream):
    tool_called_name = "None"
    final_response = None

    for s in stream:
        # Check if a tool was called
        tool_data = s.get('tools')
        if tool_data:
            tool_messages = tool_data.get('messages')
            if tool_messages and isinstance(tool_messages, list):
                for msg in tool_messages:
                    tool_called_name = getattr(msg, 'name', 'None')

        # Check if agent returned a message
        agent_data = s.get('agent')
        if agent_data:
            messages = agent_data.get('messages')
            if messages and isinstance(messages, list):
                for msg in messages:
                    if msg.content:
                        final_response = msg.content

    return tool_called_name, final_response