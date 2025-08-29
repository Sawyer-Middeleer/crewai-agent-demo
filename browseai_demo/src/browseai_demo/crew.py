from crewai import Agent, Task, Crew, Process
from crewai_tools import MCPServerAdapter

server_params = {
    "url": "http://localhost:8001/mcp", # Replace with your actual Streamable HTTP server URL
    "transport": "streamable-http"
}

try:
    with MCPServerAdapter(server_params) as tools:
        print(f"Available tools from Streamable HTTP MCP server: {[tool.name for tool in tools]}")

        http_agent = Agent(
            role="HTTP Service Integrator",
            goal="Utilize tools from a remote MCP server via Streamable HTTP.",
            backstory="An AI agent adept at interacting with complex web services.",
            tools=tools,
            verbose=True,
        )

        http_task = Task(
            description="Perform a complex data query using a tool from the Streamable HTTP server.",
            expected_output="The result of the complex data query.",
            agent=http_agent,
        )

        http_crew = Crew(
            agents=[http_agent],
            tasks=[http_task],
            verbose=True,
            process=Process.sequential
        )
        
        result = http_crew.kickoff() 
        print("\nCrew Task Result (Streamable HTTP - Managed):\n", result)

except Exception as e:
    print(f"Error connecting to or using Streamable HTTP MCP server (Managed): {e}")
    print("Ensure the Streamable HTTP MCP server is running and accessible at the specified URL.")