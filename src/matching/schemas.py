from pydantic import Field

from src.candidates.schemas import CandidateViewSchema
from src.jobs.schemas import JobViewSchema


class CandidateView(CandidateViewSchema):
    id: int = Field(..., description="Идентификатор кандидата")

class JobView(JobViewSchema):
    ...