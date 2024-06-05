import unittest
from unittest.mock import patch
from evalsone.client import EvalsOne, SampleData

class TestEvalsOne(unittest.TestCase):
    def setUp(self):
        self.api_key = 'fake_api_key'
        self.dataset_id = 'fake_dataset_id'
        self.eo_client = EvalsOne(api_key=self.api_key, dataset_id=self.dataset_id)

    @patch('evalsone.client.requests.post')
    def test_add_sample_successful(self, mock_post):
        # Mock response object
        mock_response = mock_post.return_value
        mock_response.raise_for_status = lambda: None
        mock_response.json.return_value = {'success': True, 'data': 'Sample added successfully'}

        # Test data
        sample_data = {
            'sid': 'example_sid',
            'messages': [{'role': 'user', 'content': 'Hello, world!'}]
        }

        # Validate using Pydantic
        validated_data = SampleData(**sample_data)

        # Call the method
        response = self.eo_client.add_sample(validated_data.model_dump())

        # Assertions
        self.assertTrue(response['success'])
        self.assertEqual(response['data'], 'Sample added successfully')
        mock_post.assert_called_once_with(
            f"https://api.evalsone.com/api/sample/add",
            json=validated_data.model_dump(),
            headers={'Authorization': f'Bearer {self.api_key}', 'Content-Type': 'application/json'}
        )

if __name__ == '__main__':
    unittest.main()
