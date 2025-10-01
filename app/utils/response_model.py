from fastapi.responses import JSONResponse
from typing import Optional, Dict

def api_response(
    status_code: int,
    data: Optional[Dict] = None,
    message: str = ""):
    """
    Standard API response.
    
    Args:
        status_code (int): HTTP status code.
        data (dict, optional): Payload data for success response. Default None.
        message (str): Informative message for the response.
    
    Returns:
        JSONResponse: FastAPI JSON response with uniform structure.
    """
    response = {
        "success": True if 200 <= status_code < 300 else False,
        "data": data if data else None,
        "message": message
    }
    return JSONResponse(status_code=status_code, content=response)
