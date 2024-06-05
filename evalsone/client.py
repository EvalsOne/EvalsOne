import requests
import logging
from pydantic import BaseModel, ValidationError
from typing import List, Optional

# Setup logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Define data models
class Message(BaseModel):
    role: str
    content: str

class SampleData(BaseModel):
    messages: List[Message]
    context: Optional[List[str]] = None
    ideal: Optional[List[str]] = None

class EvalsOne:
    def __init__(self, api_key: str, sid: str, base_url: str = "https://api.evalsone.com"):
        self.api_key = api_key
        self.base_url = base_url
        self.sid = sid

    def add_sample(self, sample_data: dict):
        """
        Adds a sample to the EvalsOne platform after validating the data using Pydantic model.
        Allows 'prompt' for backward compatibility but encourages 'messages' usage.
        """
        # Backward compatibility for 'prompt'
        if 'prompt' in sample_data and 'messages' not in sample_data:
            logger.warning("The 'prompt' field is deprecated and will be removed in future versions. Use 'messages' instead.")
            sample_data['messages'] = sample_data.pop('prompt')
            
        try:
            # Validate data using Pydantic
            validated_data = SampleData(**sample_data)
        except ValidationError as e:
            logger.error(f"Data validation failed: {e.json()}")
            return {'error': 'Data validation failed', 'details': e.errors()}
        
        sample_data['sid'] = self.sid
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        url = f"{self.base_url}/api/sample/add"

        # Send request
        try:
            response = requests.post(url, json=sample_data, headers=headers)
            response.raise_for_status()
        except requests.RequestException as e:
            logger.error(f"Request failed: {e}")
            return {'error': str(e)}
        return response.json()