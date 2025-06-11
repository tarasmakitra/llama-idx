from pydantic import BaseModel, Field
from typing import Optional


class Candidate(BaseModel):
    """A representation of information about a candidate extracted from a CV.
    If any field is missing or not clearly stated, return `null` for that field. `null` as empty value not string.
    """

    name: Optional[str] = Field(
        description=(
            "The candidate's full name. "
            "If the name is missing or not clearly stated, return `null` (not 'Not provided', 'N/A', or any other value)."
        )
    )

    profession: Optional[str] = Field(
        description=(
            "The candidate's primary profession or job title"
            "If value is missing or not clearly stated, return `null` (not 'Not provided', 'N/A', or any other value)."
        )
    )

    years_of_experience: Optional[int] = Field(
        description=(
            "The total number of years the candidate has worked in their profession."
            "If value is missing or not clearly stated, return `null` (not 'Not provided', 'N/A', or any other value)."
        )
    )
