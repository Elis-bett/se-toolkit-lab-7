import httpx
from typing import Dict, List, Any, Optional
from config import Config

class LMSClient:
    def __init__(self):
        self.base_url = Config.LMS_API_BASE_URL.rstrip('/')
        self.api_key = Config.LMS_API_KEY
        self.timeout = 10.0
        
    def _get_headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def _make_request(self, endpoint: str) -> Optional[Any]:
        """Make HTTP request with error handling."""
        try:
            with httpx.Client(timeout=self.timeout) as client:
                url = f"{self.base_url}/{endpoint.lstrip('/')}"
                response = client.get(url, headers=self._get_headers())
                response.raise_for_status()
                return response.json()
        except httpx.ConnectError:
            raise Exception(f"Backend error: connection refused ({self.base_url}). Check that the services are running.")
        except httpx.TimeoutException:
            raise Exception(f"Backend error: timeout after {self.timeout}s. Backend may be overloaded.")
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                raise Exception(f"Resource not found. Endpoint: {endpoint}")
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
        labs = []
        for item in items:
            # Check various possible fields that indicate this is a lab
            item_type = item.get("type") or item.get("item_type") or item.get("kind")
            
            # If type is explicitly 'lab'
            if item_type == "lab":
                labs.append(item)
            # If there's a numeric ID and it's likely a lab (since tasks might have string IDs)
            elif isinstance(item.get("id"), int) and item.get("parent_id") is None:
                labs.append(item)
            # If it has tasks as children
            elif "tasks" in item or "children" in item:
                labs.append(item)
        
        return labs
    
    def get_pass_rates(self, lab_name: str) -> Optional[Dict[str, Any]]:
        """Get pass rates for a specific lab."""
        if not lab_name:
            raise Exception("Please specify a lab, e.g., /scores lab-04")
        
        try:
            # Try both possible endpoint formats
            try:
                data = self._make_request(f"analytics/pass-rates?lab={lab_name}")
            except Exception:
                # Try alternative endpoint
                data = self._make_request(f"analytics/scores?lab={lab_name}")
            
            # Check if data is a list (as in the actual API response)
            if isinstance(data, list):
                # Transform to expected format
                transformed = {
                    "lab": lab_name,
                    "tasks": []
                }
                for item in data:
                    transformed["tasks"].append({
                        "name": item.get("task", item.get("name", "Unknown Task")),
                        "pass_rate": item.get("avg_score", item.get("pass_rate", 0)),
                        "attempts": item.get("attempts", 0)
                    })
                return transformed
            
            return data
        except Exception as e:
            if "404" in str(e) or "not found" in str(e).lower():
                raise Exception(f"Lab '{lab_name}' not found. Use /labs to see available labs.")
            raise e
    
    def check_health(self) -> tuple[bool, str]:
        """Check if backend is healthy."""
        try:
            items = self.get_items()
            count = len(items)
            # Try to get some additional info
            labs_count = len([i for i in items if i.get("type") == "lab"])
            return True, f"✅ Backend is healthy. Found {count} total items, {labs_count} labs."
        except Exception as e:
            return False, f"❌ {str(e)}"
