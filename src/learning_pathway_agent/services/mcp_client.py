import os
import httpx


class MCPClient:
    def __init__(self):
        self.role_url = os.getenv("ROLE_MCP_URL")
        self.resource_url = os.getenv("RESOURCE_MCP_URL")
        self.progress_url = os.getenv("PROGRESS_MCP_URL")

        self.headers = {
            "Authorization": f"Bearer {os.getenv('MCP_API_KEY')}"
        }

    async def get_role(self, role: str):
        async with httpx.AsyncClient() as client:
            r = await client.get(
                f"{self.role_url}/roles/{role}",
                headers=self.headers
            )
            return r.json()

    async def get_resources(self, skill: str):
        async with httpx.AsyncClient() as client:
            r = await client.get(
                f"{self.resource_url}/resources",
                params={"skill": skill},
                headers=self.headers
            )
            return r.json()

    async def get_progress(self, student_id: str):
        async with httpx.AsyncClient() as client:
            r = await client.get(
                f"{self.progress_url}/progress/{student_id}",
                headers=self.headers
            )
            return r.json()