import phi
from phi.agent import Agent
from phi.model.groq import Groq
from phi.tools.yfinance import YFinanceTools
from phi.tools.duckduckgo import DuckDuckGo
from phi.playground import Playground, serve_playground_app
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Set API key for PHI
phi.api = os.getenv("PHI_API_KEY")
if not phi.api:
    raise EnvironmentError("PHI_API_KEY is not set in the environment variables.")

# Web Search Agent (optional, can assist in general searches)
web_search_agent = Agent(
    name="Professional Web Search Agent",
    role="Search the web to provide accurate and concise information.",
    model=Groq(id="llama3-groq-70b-8192-tool-use-preview"),
    tools=[DuckDuckGo()],
    instructions=[
        "Always include reliable sources when providing information.",
        "Summarize findings clearly and concisely.",
        "Highlight key points in bullet format where applicable.",
    ],
    markdown=True,
)

# Financial Insights Agent
finance_agent = Agent(
    name="Financial Insights Agent",
    role="Provide in-depth financial analysis and insights for specific companies.",
    model=Groq(id="llama3-groq-70b-8192-tool-use-preview"),
    tools=[
        YFinanceTools(
            stock_price=True,
            company_info=True,
            income_statements=True,
            key_financial_ratios=True,
            analyst_recommendations=True,
            technical_indicators=True,
        )
    ],
    instructions=[
        "When a user asks about a specific company, fetch its stock price, financial statements, key ratios, and analyst recommendations.",
        "Organize the response in sections for better readability:",
        "- Company Overview",
        "- Current Stock Price",
        "- Key Financial Ratios",
        "- Income Statements",
        "- Analyst Recommendations",
        "Present financial data in a table format for clarity.",
        "Highlight actionable insights and trends where applicable.",
    ],
    show_tool_calls=True,
    markdown=True,
)

# Create and serve the Playground app
app = Playground(agents=[finance_agent, web_search_agent]).get_app()

if __name__ == "__main__":
    serve_playground_app("financial_agent:app", reload=True)
