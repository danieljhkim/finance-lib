import requests
import logging
from .decorator import logw
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)

@logw
def call_api(
    url: str,
    method: str = "GET",
    params: Optional[Dict[str, Any]] = None,
    headers: Optional[Dict[str, str]] = None,
    data: Optional[Any] = None,
    timeout: int = 10
) -> Optional[Dict[str, Any]]:
    try:
        response = requests.request(
            method=method.upper(),
            url=url,
            params=params,
            headers=headers,
            json=data,
            timeout=timeout
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        logger.error(f"HTTPError: {e.response.status_code} - {e.response.text}")
    except requests.exceptions.RequestException as e:
        logger.error(f"RequestException: {e}")
    except ValueError:
        logger.error("Failed to parse JSON response.")
    
    return None