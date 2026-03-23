import httpx
from typing import Dict, List, Any, Optional
from config import Config

class LMSClient:
    def __init__(self):
        self.base_url = Config.LMS_API_BASE_URL
        self.api_key = Config.LMS_API_KEY
        self.timeout = 10.0
        
    def _get_headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def _make_request(self, endpoint: str) -> Optional[Dict[str, Any]]:
        """Make HTTP request with error handling."""
        try:
            with httpx.Client(timeout=self.timeout) as client:
                response = client.get(
                    f"{self.base_url}/{endpoint}",
                    headers=self._get_headers()
                )
                response.raise_for_status()
                return response.json()
        except httpx.ConnectError:
            raise Exception(f"Backend error: connection refused ({self.base_url}). Check that the services are running.")
        except httpx.TimeoutException:
            raise Exception(f"Backend error: timeout after {self.timeout}s. Backend may be overloaded.")
        except httpx.HTTPStatusError as e:
            raise Exception(f"Backend error: HTTP {e.response.status_code} {e.response.reason_phrase}. The backend service may be down.")
        except Exception as e:
            raise Exception(f"Backend error: {str(e)}")
    
    def get_items(self) -> List[Dict[str, Any]]:
        """Fetch all items (labs and tasks)."""
        data = self._make_request("items/")
        return data if isinstance(data, list) else []
    
    def get_labs(self) -> List[Dict[str, Any]]:
        """Filter items to only labs."""
        items = self.get_items()
        return [item for item in items if item.get("type") == "lab"]
    
    def get_pass_rates(self, lab_name: str) -> Optional[Dict[str, Any]]:
        """Get pass rates for a specific lab."""
        if not lab_name:
            raise Exception("Please specify a lab, e.g., /scores lab-04")
        
        try:
            data = self._make_request(f"analytics/pass-rates?lab={lab_name}")
            return data
        except Exception as e:
            # Re-raise with more context if needed
            if "404" in str(e):
                raise Exception(f"Lab '{lab_name}' not found. Use /labs to see available labs.")
            raise e
    
    def check_health(self) -> tuple[bool, str]:
        """Check if backend is healthy."""
        try:
            items = self.get_items()
            count = len(items)
            return True, f"Backend is healthy. {count} items available."
        except Exception as e:
            return False, str(e)
