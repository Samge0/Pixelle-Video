# Copyright (C) 2025 AIDC-AI
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Z.AI endpoint helpers for bypassing 429 rate limiting.

Provides utility functions to detect Z.AI endpoints and generate
ZCode client headers to avoid content filtering and rate limiting.
"""

from typing import Optional


def is_zai_endpoint(base_url: Optional[str]) -> bool:
    """
    Check if the base_url is a Z.AI (open.bigmodel.cn) endpoint.
    This allows us to apply Z.AI-specific workarounds for 429 errors.

    Args:
        base_url: The base URL to check

    Returns:
        True if this is a Z.AI endpoint
    """
    if not base_url:
        return False
    return "open.bigmodel.cn" in base_url and "/api/coding" in base_url


def get_zcode_headers() -> dict:
    """
    Get ZCode client headers for Z.AI API requests.
    These headers help bypass Z.AI's 429 rate limiting.

    Returns:
        Dictionary of ZCode-specific headers
    """
    return {
        "User-Agent": "ZCode/0.14.8",
        "X-ZCode-App-Version": "0.14.8",
        "X-ZCode-Agent": "glm",
    }
