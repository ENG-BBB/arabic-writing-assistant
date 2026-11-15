# Connect to AI clients

Arabic Writing Assistant is an MCP server, so one server implementation can work with different AI clients. Compatibility depends on the client that runs the model and supports MCP; it is not a model-specific plugin. The server currently exposes read-only language tools over stdio and Streamable HTTP.

## Install locally

Clone or download this repository, install Python 3.11+ and `uv`, then install the project dependencies:

```sh
uv sync
```

For local clients that launch MCP servers over stdio, use this command from the project directory:

```sh
uv run mcp run server.py
```

The project directory is the folder containing `server.py` and `pyproject.toml`.

For clients that connect over HTTP, start the server:

```sh
uv run python server.py
```

Its local MCP endpoint is `http://127.0.0.1:8000/mcp` by default. The server reads `PORT` from the environment for hosting platforms and keeps the `/mcp` path. A hosted client such as ChatGPT needs a reachable HTTPS MCP endpoint or a supported secure tunnel; `localhost` on your computer is not reachable from ChatGPT's servers.

## Client support

| Client | Connection method | Notes |
| --- | --- | --- |
| ChatGPT web | HTTPS Streamable HTTP or Secure MCP Tunnel | Custom MCP availability depends on the ChatGPT plan and workspace settings. |
| Claude Desktop / Claude Code | Local stdio; Claude.ai can use remote MCP connectors where available | Configure the stdio command below or use Claude's MCP settings. |
| Qwen Code | Local stdio or remote Streamable HTTP | Add it through `qwen mcp` or `settings.json`. |
| Kimi Code CLI / Desktop | Local stdio or remote Streamable HTTP | Add it through `kimi mcp` or `mcp.json`. |
| DeepSeek | MCP-capable host, such as DeepSeek Harness, using stdio or Streamable HTTP | DeepSeek's model/API is not itself a general MCP client. A host or adapter must connect to MCP and pass tool calls/results to the model. |

## Claude Code

From any terminal, replace the path with the absolute path to this project:

```sh
claude mcp add --transport stdio arabic-writing -- uv run --directory "/absolute/path/Arabic Writing Assistant" mcp run server.py
```

Check the connection with `claude mcp list`, then ask Claude to review Arabic text or look up a grammar rule.

## Qwen Code

For a locally running server, use the `http://` endpoint only from a client on the same machine:

```sh
qwen mcp add --transport http arabic-writing http://127.0.0.1:8000/mcp
```

For local stdio, add an entry to Qwen Code's `settings.json` under `mcpServers`:

```json
{
  "mcpServers": {
    "arabic-writing": {
      "command": "uv",
      "args": ["run", "--directory", "/absolute/path/Arabic Writing Assistant", "mcp", "run", "server.py"]
    }
  }
}
```

Restart Qwen Code and use `/mcp` to check that the tools were discovered.

## Kimi Code

For a locally running server:

```sh
kimi mcp add --transport http arabic-writing http://127.0.0.1:8000/mcp
kimi mcp test arabic-writing
```

For local stdio, add an `arabic-writing` entry to Kimi Code's `mcp.json`:

```json
{
  "mcpServers": {
    "arabic-writing": {
      "command": "uv",
      "args": ["run", "--directory", "/absolute/path/Arabic Writing Assistant", "mcp", "run", "server.py"]
    }
  }
}
```

## ChatGPT web

ChatGPT connects to remote MCP servers, not directly to a process running on your computer. Start the server and either deploy it at a stable HTTPS URL ending in `/mcp`, or configure OpenAI Secure MCP Tunnel to keep it private. In ChatGPT web, open **Plugins**, select **+**, choose **Add custom MCP server**, enter the endpoint (or choose **Tunnel**), review the discovered tools, and create the plugin. Account and workspace access rules apply.

## DeepSeek

DeepSeek API function calling and MCP are separate pieces. To use this server with a DeepSeek model, select DeepSeek in an MCP-capable agent host that supports custom models, or use a host with a DeepSeek MCP client. For example, DeepSeek Harness documents an MCP client that connects to stdio servers and Streamable HTTP servers. The standard DeepSeek chat website should not be assumed to accept arbitrary MCP server URLs unless its current product settings explicitly offer that feature.

## Security and limits

- The application code has no database or file-writing logic and does not call an external model or language API. It processes the supplied text for the current tool call and returns language guidance; the connected AI client also receives the text under its own data policies.
- Hosting providers may keep operational logs according to their own settings and policies. Review those settings before deployment; the application code cannot control provider-level retention.
- The HTTP endpoint currently has no authentication or rate limiting. Keep it on localhost or use a private tunnel until you add appropriate access controls before public exposure.
- MCP support belongs to the host application. A model may support tool calling through an API while the associated consumer chat interface does not support custom MCP servers.
- MCP tool use can increase prompt context because the returned rule and dictionary content is sent to the model.

## Official client references

- [ChatGPT custom MCP servers](https://help.openai.com/en/articles/12584461-connecting-custom-mcp-servers-in-chatgpt)
- [OpenAI Secure MCP Tunnel](https://developers.openai.com/api/docs/guides/secure-mcp-tunnels)
- [Anthropic MCP documentation](https://docs.anthropic.com/en/docs/mcp)
- [Qwen Code MCP guide](https://github.com/QwenLM/qwen-code/blob/main/docs/users/features/mcp.md)
- [Kimi Code MCP guide](https://github.com/MoonshotAI/kimi-code/blob/main/docs/en/customization/mcp.md)
- [Kimi CLI MCP commands](https://github.com/MoonshotAI/kimi-cli/blob/main/docs/en/reference/kimi-mcp.md)
- [DeepSeek Harness MCP client](https://github.com/deepseek-ai/deepseek-harness/tree/master/packages/mcp/mcp-client)
