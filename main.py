from typing import Any
from mcp.server.fastmcp import FastMCP
from lib.mythic_api import MythicAPI
import asyncio
import base64
import sys
import argparse
import json

mcp = FastMCP("mythic_mcp")

api = None


@mcp.prompt()
def start_pentest(threat_actor: str, objective: str) -> str:
    return f"You are an automated pentester, tasked with emulating a specific threat actor. The threat actor is {threat_actor}. Your objective is: {objective}. Perform any required steps to meet the objective, using only techniques documented by the threat actor."


@mcp.prompt()
def start_recon() -> str:
    return "You are an automated pentester, tasked with performing recon. Use the available agents to gather information on the compromised hosts."


@mcp.tool()
async def run_as_user(agent_id: int, username: str, password: str):
    """Attempt to authenticate as another user (network calls only) for the current session.

    Args:
        username: Username of network account to use
        password: Password of network account
    """

    output = await api.make_token(agent_id, username, password)

    return f"---\nAuthentication Result: {output}\n---"


@mcp.tool()
async def execute_mimikatz(agent_id: int, mimikatz_arguments: str):
    """Runs the hacker tool mimikatz with the provided arguments, returing Mimikatz output.

    Args:
        mimikatz_arguments: Arguments to pass to mimikatz tool
    """

    output = await api.execute_mimikatz(agent_id, mimikatz_arguments)

    return f"---\n{output}\n---"


@mcp.tool()
async def read_file(agent_id: int, file_path: str):
    """Reads a file using the ReadFile win32 API call. Returns the contents of that file.

    Args:
        agent_id: ID of agent to read file from
        file_path: Path to the file to read on the target server
    """

    output = await api.read_file(agent_id, file_path)

    return f"---\n{output}\n---"


@mcp.tool()
async def run_shell_command(agent_id: int, command_line: str):
    """Execute a shell script command line against a running agent. This script is executed using the default command line interpreter.

    Args:
        agent_id: ID of agent to execute command on
        command_line: A command to be executed
    """

    output = await api.execute_shell_command(agent_id, command_line)

    return f"---\n{output}\n---"


@mcp.tool()
async def get_all_agents():
    """Returns a list of active Mythic agents"""

    return json.dumps(await api.get_all_agents())


@mcp.tool()
async def upload_file(agent_id: int, file_name: str, remote_path: str, content: str):
    """Upload a file to the Mythic server, and then upload the file to the remote target

    Args:
        agent_id: ID of the agent to execute command on
        file_name: Name to give the file when uploading to Mythic server
        remote_path: Full path to where the file will be uploaded
        content: Base64 encoded contents of the file
    """

    decoded_contents = base64.b64decode(content)
    status = await api.upload_file(agent_id, file_name, remote_path, decoded_contents)

    if status:
        return "---\nFile uploaded successfully\n---"
    else:
        return "---\nError uploading file\n---"


async def main():
    await api.connect()
    await mcp.run_stdio_async()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="MCP for Mythic")
    parser.add_argument(
        "username", type=str, help="Username used to connect to Mythic API"
    )
    parser.add_argument(
        "password", type=str, help="Password used to connect to Mythic API"
    )
    parser.add_argument("host", type=str, help="Host (IP or DNS) of Mythic API server")
    parser.add_argument("port", type=str, help="Port of Mythic server HTTP server")

    args = parser.parse_args()
    api = MythicAPI(args.username, args.password, args.host, args.port)

    asyncio.run(main())
