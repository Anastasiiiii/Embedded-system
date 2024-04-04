# pylint: disable=all
import json
import logging
from typing import List
import pydantic_core
import requests  # type: ignore
from app.entities.processed_agent_data import ProcessedAgentData
from app.interfaces.store_gateway import StoreGateway

class StoreApiAdapter(StoreGateway):
    def __init__(self, api_base_url):
        self.api_base_url = api_base_url

    def save_data(self, processed_agent_data_batch: List[ProcessedAgentData]):
        try:
            # Convert processed data to JSON
            processed_data_json = [data.dict() for data in processed_agent_data_batch]
            
            # Make a POST request to the Store API endpoint with the processed data
            response = requests.post(f"{self.api_base_url}/endpoint", json=processed_data_json)

            # Check response status code
            if response.status_code == 200:
                logging.info("Data saved successfully.")
                return True
            else:
                logging.error(f"Failed to save data. Status code: {response.status_code}")
                return False
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            return False
