summary_prompt = """
Given the following candidate information, generate a concise summary (2–3 sentences) that 
highlights the candidate's strongest skills, key professional achievements and career highlights
"""


details_prompt = """
Given the following candidate CV text, extract the following fields:
- `name`: The full name of the candidate (if mentioned).
- `profession`: The candidate's profession or job title (e.g., Software Engineer, Project Manager).
- `years_of_experience`: The total number of years of commercial/professional experience the candidate has.

Return the result in a valid JSON object with these keys: "name" (string), "profession" (string), 
"years_of_experience" (integer). If any field is missing or not clearly stated, 
return `null` for that field. Output only the JSON.

Example output:
{{
    "name": "Jane Doe",
    "profession": "Data Scientist",
    "years_of_experience": 5
}}

Now extract from this text:
{text}
"""
