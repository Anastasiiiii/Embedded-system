# pylint: disable=all
import json
import logging
from typing import List
import requests # type: ignore
from app.entities.processed_agent_data import ProcessedAgentData
from app.interfaces.store_gateway import StoreGateway

class StoreApiAdapter(StoreGateway):
    def __init__(self, api_base_url):
        self.api_base_url = api_base_url

    def save_data(self, processed_agent_data_batch: List[ProcessedAgentData]):
        try:
            # Prepare data for POST request
            data = [processed_agent_data.dict() for processed_agent_data in processed_agent_data_batch]
            json_data = json.dumps(data)
            
            # Make a POST request to the Store API endpoint
            response = requests.post(f"{self.api_base_url}/processed_agent_data", json=json_data)
            
            # Check if request was successful
            if response.status_code == 200:
                logging.info("Data saved successfully to the Store API.")
            else:
                logging.error(f"Failed to save data to the Store API. Status code: {response.status_code}")
        except Exception as e:
            logging.error(f"An error occurred while saving data to the Store API: {str(e)}")
