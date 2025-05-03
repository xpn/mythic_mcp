[![MseeP.ai Security Assessment Badge](https://mseep.net/pr/xpn-mythic-mcp-badge.png)](https://mseep.ai/app/xpn-mythic-mcp)

# Mythic MCP

A quick MCP demo for Mythic, allowing LLMs to pentest on our behalf!

## Requirements

1. uv
2. python3
3. Claude Desktop (or other MCP Client)

## Usage with Claude Desktop

To deploy this MCP Server with Claude Desktop, you'll need to edit your `claude_desktop_config.json` to add the following:

```
{
    "mcpServers": {
        "mythic_mcp": {
            "command": "/Users/xpn/.local/bin/uv",
            "args": [
                "--directory",
                "/full/path/to/mythic_mcp/",
                "run",
                "main.py",
                "mythic_admin",
                "mythic_admin_password",
                "localhost",
                "7443"
            ]
        }
    }
}
```

Once done, kick off Claude Desktop. There are sample prompts to show how to task the LLM, but really anything will work along the lines of:

```
You are an automated pentester, tasked with emulating a specific threat actor. The threat actor is APT31. Your objective is: Add a flag to C:\win.txt on DC01. Perform any required steps to meet the objective, using only techniques documented by the threat actor.
```
