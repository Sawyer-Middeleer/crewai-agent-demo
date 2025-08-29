#!/usr/bin/env python
import sys
import warnings

from crewai import Agent, Task, Crew, Process
from crewai_tools import MCPServerAdapter

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

server_params = {
    "url": "http://localhost:8001/mcp",  # Replace with your actual Streamable HTTP server URL
    "transport": "streamable-http",
}


def _build_http_crew(tools: list) -> Crew:
    """Construct the MCP-backed HTTP crew using provided tools."""
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

    return Crew(
        agents=[http_agent],
        tasks=[http_task],
        verbose=True,
        process=Process.sequential,
    )


def run():
    """Run the crew using the MCP-backed HTTP tools."""
    try:
        with MCPServerAdapter(server_params) as tools:
            crew = _build_http_crew(tools)
            result = crew.kickoff()
            print("\nCrew Task Result (Streamable HTTP - Managed):\n", result)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


def train():
    """Train the crew for a given number of iterations."""
    try:
        n_iterations = int(sys.argv[1])
        filename = sys.argv[2]
        with MCPServerAdapter(server_params) as tools:
            crew = _build_http_crew(tools)
            crew.train(n_iterations=n_iterations, filename=filename)
    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")


def replay():
    """Replay the crew execution from a specific task."""
    try:
        task_id = sys.argv[1]
        with MCPServerAdapter(server_params) as tools:
            crew = _build_http_crew(tools)
            crew.replay(task_id=task_id)
    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")


def test():
    """Test the crew execution and returns the results."""
    try:
        n_iterations = int(sys.argv[1])
        eval_llm = sys.argv[2]
        with MCPServerAdapter(server_params) as tools:
            crew = _build_http_crew(tools)
            crew.test(n_iterations=n_iterations, eval_llm=eval_llm)
    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")
