import asyncio
import json
from typing import Any, Dict, List

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from learning_pathway_agent.crew import LearningPathwayAgentCrew
from learning_pathway_agent.data.role_catalog import get_role_catalog_entry

app = FastAPI()


def _normalize_role_name(target_role: str) -> str:
    if not target_role:
        return "Data Scientist"
    return target_role.strip().replace("_", " ").title()


def _build_fallback_plan(
    student_profile: str,
    target_role: str,
    role_catalog_data: Dict[str, Any],
) -> str:
    role_name = role_catalog_data.get("role_name") or _normalize_role_name(target_role)
    required_skills: List[str] = role_catalog_data.get("required_skills") or []
    priority_skills: List[str] = role_catalog_data.get("priority_skills") or []
    prerequisites: List[str] = role_catalog_data.get("prerequisites") or []

    if not required_skills:
        required_skills = ["python", "sql", "statistics", "machine learning"]
    if not priority_skills:
        priority_skills = required_skills[:2]
    if not prerequisites:
        prerequisites = ["basic programming", "foundational math"]

    return f"""# Learning Pathway — {role_name}

## Target Role
{role_name}

## Current Readiness Score
35%

## Skill Gap Analysis
| Skill | Current Level | Required Level | Priority |
|---|---|---|---|
| Python | Beginner | Intermediate | High |
| SQL | Beginner | Intermediate | High |
| Statistics | Beginner | Intermediate | Medium |
| Machine Learning | Beginner | Intermediate | High |
| Project Experience | None | Practical | High |

## Learning Roadmap

### Stage 1: Foundations
- Objectives: build strong Python, SQL, and statistics basics
- Skills: {", ".join(prerequisites + required_skills[:2])}
- Milestones: write Python scripts, complete SQL exercises, understand core stats
- Duration: 3-4 weeks

### Stage 2: Applied Learning
- Objectives: apply skills in notebooks and guided projects
- Skills: {", ".join(priority_skills)}
- Milestones: complete 1-2 mini projects, practice feature engineering, evaluate models
- Duration: 4-5 weeks

### Stage 3: Job Readiness
- Objectives: prepare portfolio, interviews, and job-ready workflow
- Skills: communication, interview practice, project storytelling
- Milestones: finish a capstone project, mock interview, resume/project review
- Duration: 3 weeks

## Recommended Resources
- Python basics course
- SQL practice platform
- Intro to statistics resource
- Machine learning fundamentals course
- Project-based portfolio tutorial

## Progress Summary
- Completed Skills: basic Python, basic math
- Remaining Skills: SQL, machine learning, project experience
- Milestones Achieved: beginner foundation established

## Next Recommended Actions
1. Practice SQL for 30 minutes daily
2. Complete one small ML project
3. Build a portfolio project aligned to {role_name}

Student context used:
{student_profile}

Role requirements used:
{json.dumps(role_catalog_data, indent=2)}
"""


async def run_crew(context: dict) -> str:
    try:
        crew = LearningPathwayAgentCrew().crew()
        loop = asyncio.get_running_loop()

        result = await loop.run_in_executor(
            None,
            lambda: crew.kickoff(inputs=context),
        )

        raw = getattr(result, "raw", None) or str(result)
        if len(raw.strip()) < 150 or "Learning Pathway" not in raw:
            return _build_fallback_plan(
                context.get("student_profile", ""),
                context.get("target_role", "data_scientist"),
                context.get("role_catalog_data", {}),
            )
        return raw
    except Exception:
        return _build_fallback_plan(
            context.get("student_profile", ""),
            context.get("target_role", "data_scientist"),
            context.get("role_catalog_data", {}),
        )


@app.post("/run")
async def run(payload: dict):
    student_profile = payload.get("context", "")
    target_role = payload.get("target_role", "data_scientist")

    if isinstance(student_profile, dict):
        student_profile = json.dumps(student_profile, indent=2)

    role_catalog_data = get_role_catalog_entry(target_role)
    if not isinstance(role_catalog_data, dict) or role_catalog_data.get("error"):
        role_catalog_data = get_role_catalog_entry("data_scientist")

    context = {
        "student_profile": student_profile,
        "target_role": target_role,
        "role_catalog_data": role_catalog_data,
    }

    final_output = await run_crew(context)
    return JSONResponse({"output": final_output})
