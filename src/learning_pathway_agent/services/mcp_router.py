from src.learning_pathway_agent.services.mcp_client import MCPClient


class MCPRouter:
    def __init__(self):
        self.internal = MCPClient()

    async def query(self, source: str, payload: dict):

        # -------------------------
        # INTERNAL MCP (YOUR SYSTEM)
        # -------------------------
        if source == "role":
            return await self.internal.get_role(payload["role"])

        if source == "resources":
            return await self.internal.get_resources(payload["skill"])

        if source == "progress":
            return await self.internal.get_progress(payload["student_id"])

        # -------------------------
        # EXTERNAL MCP (PUBLIC TOOLS)
        # -------------------------
        if source == "ddgs_search":
            return self.ddgs_search(payload["query"])

        if source == "brave_search":
            return self.brave_search(payload["query"])

        raise ValueError(f"Unknown MCP source: {source}")

    # ---- external tools (simple stubs for now)
    def ddgs_search(self, query):
        return f"[DDGS MOCK RESULT for {query}]"

    def brave_search(self, query):
        return f"[BRAVE MOCK RESULT for {query}]"