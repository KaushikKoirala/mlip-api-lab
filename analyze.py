import json
import os
from typing import Any, Dict, List
from litellm import completion
from pydantic import BaseModel, Field, ValidationError
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# You can replace these with other models as needed but this is the one we suggest for this lab.
MODEL = "groq/llama-3.3-70b-versatile"


class ItinerarySchema(BaseModel):
    """Schema for validating itinerary responses."""
    destination: str = Field(..., description="The travel destination")
    price_range: str = Field(..., description="Price range for the trip (e.g., budget, moderate, luxury)")
    ideal_visit_times: List[str] = Field(..., description="Best times to visit (e.g., seasons or months)")
    top_attractions: List[str] = Field(..., description="List of top attractions to visit")


def get_itinerary(destination: str) -> Dict[str, Any]:
    """
    Returns a JSON-like dict with keys:
      - destination
      - price_range
      - ideal_visit_times
      - top_attractions

    The response is validated against a predefined schema using Pydantic.

    Args:
        destination: The destination to generate an itinerary for

    Returns:
        Dict containing validated itinerary data

    Raises:
        ValueError: If API key is missing or response validation fails
        Exception: If API call fails
    """
    # Get API key from environment variable
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY not found in environment variables. Please set it in .env file.")

    # Set environment variable for Groq API (required by litellm)
    os.environ["GROQ_API_KEY"] = api_key

    # Create prompt for structured travel itinerary
    prompt = f"""Generate a travel itinerary for {destination} in JSON format with the following structure:
    {{
        "destination": "{destination}",
        "price_range": "budget/moderate/luxury",
        "ideal_visit_times": ["season1", "season2"],
        "top_attractions": ["attraction1", "attraction2", "attraction3"]
    }}

    Provide only the JSON response without any additional text."""

    # Make litellm API call
    response = completion(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"}
    )

    # Extract and parse the response
    content = response.choices[0].message.content
    data = json.loads(content)

    # Validate response against schema
    try:
        validated_itinerary = ItinerarySchema(**data)
        return validated_itinerary.model_dump()
    except ValidationError as e:
        raise ValueError(f"Response validation failed: {e}")
