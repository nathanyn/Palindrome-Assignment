from langchain.agents import AgentExecutor, create_react_agent
from langchain import hub
from langchain_openai import ChatOpenAI
from langchain.tools import Tool
import config

# 1. Create the model
model = ChatOpenAI(openai_api_key=config.OPENAI_API_KEY)

# 2. Create the tools
def count_characters_in_string(string: str) -> str:
    return len(string)

def is_palindrome(string: str) -> str:
    return string == string[::-1]

tools = [
    Tool.from_function(
        func=count_characters_in_string,
        name="Count Characters in a text string",
        description="Count the number of characters in a text string",
    ),
    Tool.from_function(
        func=is_palindrome,
        name="Check if a word is a palindrome",
        description="Check if a given word is a palindrome",
    )
]

# 3. Get the prompt to use
prompt = hub.pull("hwchase17/react",api_key=config.LANGSMITH_API_KEY)

# 4. Construct the ReAct agent
agent = create_react_agent(model, tools, prompt)

# 5. Create an agent executor by passing in the agent and tools
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# 6. Invoke the agent executor
agent_executor.invoke({"input": 'Is the word "radar" a palindrome?'})
