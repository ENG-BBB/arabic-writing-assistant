import asyncio
import json

from mcp import Client
import server


def test_mcp_tools_are_discoverable_and_callable():
    async def check_tools():
        async with Client(server.server) as client:
            tools = await client.list_tools()
            names = {tool.name for tool in tools.tools}
            assert names == {
                "search_arabic_rules",
                "audit_arabic_punctuation",
                "disambiguate_arabic_word",
                "review_arabic_text",
            }
            result = await client.call_tool(
                "disambiguate_arabic_word",
                {"word": "ملك", "context": "حكم الملك البلاد"},
            )
            assert not result.is_error
            payload = json.loads(result.content[0].text)
            assert payload["matches"]

    asyncio.run(check_tools())
