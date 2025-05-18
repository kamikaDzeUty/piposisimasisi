# src/infrastructure/tbank_client.py
import os
import requests
from typing import List, Dict

class TBankClient:
    """
    HTTP-клиент для работы с API Т-Банка.
    """
    def __init__(self, base_url: str = "https://api.tbank.example.com", api_key: str = 'invest-public-api.tinkoff.ru:443.', timeout: int = 10):
        self.base_url = base_url or os.getenv("TBANK_API_BASE_URL")
        self.api_key = api_key or os.getenv("TBANK_API_KEY")
        if not self.base_url or not self.api_key:
            raise ValueError("TBANK_API_BASE_URL and TBANK_API_KEY must be set")
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        })

    def list_assets(self, asset_type: str) -> List[Dict]:
        url = f"{self.base_url}/assets/{asset_type}s"
        response = self.session.get(url, timeout=self.timeout)
        response.raise_for_status()
        return response.json().get('data', [])

    def get_price_history(self, symbol: str, period: int) -> List[float]:
        url = f"{self.base_url}/prices/{symbol}"
        params = {"period": period}
        response = self.session.get(url, params=params, timeout=self.timeout)
        response.raise_for_status()
        data = response.json().get('prices', [])
        return [item['price'] for item in data]