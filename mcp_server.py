from mcp.server.fastmcp import FastMCP

mcp = FastMCP("SkyApp")

@mcp.tool()
def status() -> str:
    return "SkyApp MCP Server läuft reibungslos."

if __name__ == "__main__":
    mcp.run()

