#!/usr/bin/env python3
"""Debug script to test the debate API endpoint."""

import sys
import asyncio
import traceback

# Add the current directory to Python path
sys.path.append('.')

from app.models.schemas import DebateRequest
from app.api.routes import debate

async def test_debate():
    """Test the debate endpoint directly."""
    try:
        print("Creating request...")
        request = DebateRequest(
            conversation_id=None,
            message="Sun rises from west, take stance sun rise from west."
        )
        
        print("Calling debate function...")
        response = await debate(request)
        
        print("Success!")
        print(f"Conversation ID: {response.conversation_id}")
        print(f"Number of messages: {len(response.message)}")
        if response.message:
            print(f"Last message: {response.message[-1].message[:100]}...")
        
        return response
        
    except Exception as e:
        print(f"Error: {e}")
        print(f"Error type: {type(e).__name__}")
        print("Traceback:")
        traceback.print_exc()
        return None

if __name__ == "__main__":
    result = asyncio.run(test_debate())
    if result:
        print("Test completed successfully!")
    else:
        print("Test failed!")
