import base64
import openai  # Correct import of the OpenAI library
import logging
from openai import APIConnectionError, RateLimitError, AuthenticationError
from pydantic import BaseModel, ValidationError
from app.config import settings
from dotenv import load_dotenv
from typing import Optional


load_dotenv()

# Instantiate the client with the API key from settings (or environment)
client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)

# Configure logging
logging.basicConfig(
    filename="app_logs.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Define the expected structured response using Pydantic.
class PartInspectionResult(BaseModel):
    recognized_part: str
    defect_status: str
    defect_type: Optional[str] = None
    confidence: float

class OpenAIService:
    async def call_model(self, file_content: bytes) -> dict:
        # Encode the image as a base64 string
        base64_image = base64.b64encode(file_content).decode("utf-8")

        # Prepare the messages with both text and image as per the official examples
        messages = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": (
                            "Analyze this automobile part and return a JSON object with these fields:\n"
                            "- recognized_part (string): Name of the automobile part\n"
                            "- defect_status (string): 'Defective' or 'Not Defective'\n"
                            "- defect_type (string or null): If defective, either 'Manufacturing Defect' or 'Customer Abuse'; otherwise, null\n"
                            "- confidence (number): A value between 0 and 1\n\n"
                            "Return only valid JSON, with no extra text."
                        ),
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                    },
                ],
            }
        ]
       
        try:
            # Use the client to call the chat completions endpoint as per the official docs
            response = client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=messages
            )
            result_text = response.choices[0].message.content
            logger.info(f"API Call Success: {result_text}")

        except APIConnectionError:
            return {"error": "AI model API call failed: Unable to connect to OpenAI."}
        except RateLimitError:
            return {"error": "AI model API call failed: Rate limit exceeded."}
        except AuthenticationError:
            return {"error": "AI model API call failed: Invalid API key."}
        except Exception as e:
            return {"error": f"Unexpected error occurred: {str(e)}"}

        # Clean the returned text
        cleaned_text = result_text.strip()
        if cleaned_text.startswith("```json"):
            cleaned_text = cleaned_text.strip("```json").strip("```")

        try:
            # Validate and parse the JSON using Pydantic
            result_obj = PartInspectionResult.parse_raw(cleaned_text)
            logger.info(f"Successfully parsed response: {result_obj.dict()}")
            return result_obj.dict()

        except ValidationError as e:
            return {"error": f"Unable to parse AI model response: {e}"}
