import asyncio
import json

from fastapi import FastAPI
from fastapi.responses import StreamingResponse

from learning_pathway_agent.crew import LearningPathwayAgentCrew
from learning_pathway_agent.data.role_catalog import get_role_catalog_entry

app = FastAPI()


async def run_crew(queue: asyncio.Queue, context: dict):
    try:
        crew = LearningPathwayAgentCrew().crew()
        loop = asyncio.get_running_loop()

        result = await loop.run_in_executor(
            None,
            lambda: crew.kickoff(inputs=context),
        )

        await queue.put(f"[FINAL]{result}")
    except Exception as e:
        await queue.put(f"[ERROR]{str(e)}")


@app.post("/run")
async def run(payload: dict):
    queue: asyncio.Queue = asyncio.Queue()

    student_profile = payload.get("context", "")
    target_role = payload.get("target_role", "data_scientist")

    if isinstance(student_profile, dict):
        student_profile = json.dumps(student_profile, indent=2)

    role_catalog_data = get_role_catalog_entry(target_role)
    if "error" in role_catalog_data:
        role_catalog_data = get_role_catalog_entry("data_scientist")

    context = {
        "student_profile": student_profile,
        "target_role": target_role,
        "role_catalog_data": role_catalog_data,
    }

    asyncio.create_task(run_crew(queue, context))

    async def stream():
        while True:
            msg = await queue.get()
            yield f"data: {msg}\n\n"

            if msg.startswith("[FINAL]") or msg.startswith("[ERROR]"):
                break

    return StreamingResponse(stream(), media_type="text/event-stream")
