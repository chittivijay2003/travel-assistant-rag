"""
Visible Test Script for RAG Travel Assistant API (Assignment D4)
===============================================================
This script performs BASIC SANITY CHECKS on the /rag-travel endpoint.
It validates the OpenAPI specification compliance and outputs a final score.

Students receive this file to verify their API works before submission.
"""

import requests
import json
import sys
import os
from typing import Dict, Any, Tuple, List
from datetime import datetime
import time
from dotenv import load_dotenv

load_dotenv()

# =============================================================================
# CONFIGURATION
# =============================================================================
BASE_URL = f"http://localhost:{os.getenv('API_PORT', '8000')}"
ENDPOINT = "/rag-travel"
OUTPUT_FILE = "d4_output.txt"


# =============================================================================
# HELPER CLASSES
# =============================================================================
class Colors:
    """ANSI color codes for terminal output"""

    GREEN = "\033[92m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    RESET = "\033[0m"
    BOLD = "\033[1m"


class Logger:
    """Dual logger: writes to both console and file"""

    def __init__(self, filename: str):
        self.filename = filename
        with open(self.filename, "w", encoding="utf-8") as f:
            f.write(f"{'=' * 70}\n")
            f.write(
                f"RAG Travel Assistant API (D4) Test Run: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            )
            f.write(f"{'=' * 70}\n\n")

    def log(self, message: str, color: str = "", file_only: bool = False):
        if not file_only:
            print(f"{color}{message}{Colors.RESET if color else ''}")
        with open(self.filename, "a", encoding="utf-8") as f:
            f.write(message + "\n")


# Initialize logger
logger = Logger(OUTPUT_FILE)


# =============================================================================
# VALIDATION FUNCTIONS
# =============================================================================
def validate_response_structure(data: Dict[str, Any]) -> Tuple[bool, str]:
    """
    Validates that the API response matches the OpenAPI specification.

    Required fields:
    - answer (string, non-empty)
    - retrieved_context (array of objects)
    - debug (optional object)

    Each retrieved_context item must have:
    - id (string)
    - text (string)
    - score (number)
    """
    # Check answer field
    if "answer" not in data:
        return False, "Missing required field: answer"
    if not isinstance(data["answer"], str):
        return False, "Field 'answer' must be a string"
    if len(data["answer"].strip()) == 0:
        return False, "Field 'answer' cannot be empty"

    # Check retrieved_context field
    if "retrieved_context" not in data:
        return False, "Missing required field: retrieved_context"
    if not isinstance(data["retrieved_context"], list):
        return False, "Field 'retrieved_context' must be an array"
    if len(data["retrieved_context"]) == 0:
        return False, "Field 'retrieved_context' must contain at least one item"

    # Validate each context item
    for i, item in enumerate(data["retrieved_context"]):
        if not isinstance(item, dict):
            return False, f"retrieved_context[{i}] must be an object"

        # Check required fields in context item
        required_fields = ["id", "text", "score"]
        for field in required_fields:
            if field not in item:
                return False, f"retrieved_context[{i}] missing required field: {field}"

        # Check field types
        if not isinstance(item["id"], str):
            return False, f"retrieved_context[{i}].id must be a string"
        if not isinstance(item["text"], str):
            return False, f"retrieved_context[{i}].text must be a string"
        if not isinstance(item["score"], (int, float)):
            return False, f"retrieved_context[{i}].score must be a number"

        # Check field values
        if len(item["id"].strip()) == 0:
            return False, f"retrieved_context[{i}].id cannot be empty"
        if len(item["text"].strip()) == 0:
            return False, f"retrieved_context[{i}].text cannot be empty"

    # Optional debug field validation
    if "debug" in data and not isinstance(data["debug"], dict):
        return False, "Field 'debug' must be an object if present"

    return True, "Response structure is valid"


def validate_content_quality(data: Dict[str, Any], query: str) -> Tuple[bool, str]:
    """
    Basic content quality checks.
    - Answer should be substantial (> 50 characters)
    - Retrieved context should contain travel-related content
    - Answer should be more than just a copy of context
    """
    answer = data.get("answer", "")
    retrieved_context = data.get("retrieved_context", [])

    # Answer length check
    if len(answer) < 50:
        return (
            False,
            f"Answer too brief ({len(answer)} chars). Expected substantial response.",
        )

    # Context relevance check
    travel_keywords = [
        "visa",
        "travel",
        "passport",
        "country",
        "destination",
        "trip",
        "tourist",
        "embassy",
        "requirement",
        "document",
    ]
    context_text = " ".join(
        [item.get("text", "") for item in retrieved_context]
    ).lower()

    if not any(keyword in context_text for keyword in travel_keywords):
        return (
            False,
            "Retrieved context doesn't appear to contain travel-related information",
        )

    # Answer should not be just a copy of first context
    if len(retrieved_context) > 0:
        first_context = retrieved_context[0].get("text", "")
        if first_context.lower().strip() == answer.lower().strip():
            return False, "Answer appears to be a direct copy of retrieved context"

    # Check if answer mentions key terms from query
    query_lower = query.lower()
    answer_lower = answer.lower()

    # Extract potential destination/country from query
    common_countries = [
        "japan",
        "india",
        "thailand",
        "usa",
        "france",
        "germany",
        "italy",
        "spain",
        "canada",
        "australia",
    ]
    query_countries = [
        country for country in common_countries if country in query_lower
    ]

    if query_countries and not any(
        country in answer_lower for country in query_countries
    ):
        return (
            False,
            f"Answer doesn't mention destination/country from query: {query_countries}",
        )

    return True, "Content quality validation passed"


def validate_rag_functionality(data: Dict[str, Any]) -> Tuple[bool, str]:
    """
    Validate that RAG functionality is working:
    - Retrieved context has reasonable scores
    - Multiple context items if available
    - Scores are in reasonable range
    """
    retrieved_context = data.get("retrieved_context", [])

    if len(retrieved_context) == 0:
        return False, "No retrieved context - RAG not functioning"

    # Check score distribution
    scores = [item.get("score", 0) for item in retrieved_context]

    # Scores should be in reasonable range (0.0 to 1.0 or similar)
    if any(score < 0 for score in scores):
        return False, "Retrieved context contains negative scores"

    if any(score > 10 for score in scores):
        return False, "Retrieved context contains unrealistically high scores (>10)"

    # If multiple contexts, scores should generally be in descending order (best first)
    if len(scores) > 1:
        descending = all(scores[i] >= scores[i + 1] for i in range(len(scores) - 1))
        if not descending:
            return (
                False,
                "Retrieved context scores should be in descending order (most relevant first)",
            )

    # Check for diversity in retrieved context (not all identical)
    texts = [item.get("text", "") for item in retrieved_context]
    if len(texts) > 1 and len(set(texts)) == 1:
        return (
            False,
            "All retrieved context items are identical - poor retrieval diversity",
        )

    return True, "RAG functionality validation passed"


# =============================================================================
# TEST EXECUTION
# =============================================================================
def run_test(
    test_name: str, payload: Dict[str, Any], expect_success: bool = True
) -> Dict[str, Any]:
    """
    Runs a single test against the API endpoint.

    Returns:
        Dict with 'passed' and 'message' keys
    """
    logger.log(f"\n{'=' * 70}", Colors.BLUE)
    logger.log(f"{test_name}", Colors.BLUE + Colors.BOLD)
    logger.log(f"{'=' * 70}", Colors.BLUE)
    logger.log(f"Payload: {json.dumps(payload, indent=2)}")

    result = {"passed": False, "message": ""}

    try:
        start_time = time.time()
        response = requests.post(
            f"{BASE_URL}{ENDPOINT}", json=payload, timeout=300
        )  # 5 min timeout for RAG
        end_time = time.time()

        response_time = (end_time - start_time) * 1000  # Convert to milliseconds
        logger.log(f"Response time: {response_time:.0f}ms")

        if expect_success:
            # Test should return 200
            if response.status_code != 200:
                result["message"] = (
                    f"Expected status 200, got {response.status_code}. Response: {response.text[:200]}"
                )
                logger.log(f"❌ {result['message']}", Colors.RED)
                return result

            # Parse JSON response
            try:
                data = response.json()
                logger.log(f"Response data keys: {list(data.keys())}")
            except json.JSONDecodeError as e:
                result["message"] = f"Invalid JSON response: {e}"
                logger.log(f"❌ {result['message']}", Colors.RED)
                return result

            # Validate response structure
            is_valid_structure, structure_msg = validate_response_structure(data)
            if not is_valid_structure:
                result["message"] = f"Invalid response structure: {structure_msg}"
                logger.log(f"❌ {result['message']}", Colors.RED)
                return result

            logger.log(f"✅ Response structure valid")

            # Validate content quality
            is_valid_content, content_msg = validate_content_quality(
                data, payload.get("query", "")
            )
            if not is_valid_content:
                result["message"] = f"Content quality issue: {content_msg}"
                logger.log(f"⚠️  {result['message']}", Colors.YELLOW)
                # Don't fail test for content quality, just warn
            else:
                logger.log(f"✅ Content quality good")

            # Validate RAG functionality
            is_rag_working, rag_msg = validate_rag_functionality(data)
            if not is_rag_working:
                result["message"] = f"RAG functionality issue: {rag_msg}"
                logger.log(f"❌ {result['message']}", Colors.RED)
                return result

            logger.log(f"✅ RAG functionality working")

            # Log key response details
            logger.log(f"\n--- Response Summary ---")
            logger.log(f"Answer length: {len(data.get('answer', ''))} characters")
            logger.log(f"Retrieved contexts: {len(data.get('retrieved_context', []))}")

            if len(data.get("retrieved_context", [])) > 0:
                scores = [item.get("score", 0) for item in data["retrieved_context"]]
                logger.log(f"Score range: {min(scores):.3f} - {max(scores):.3f}")

            result["passed"] = True
            result["message"] = "Test passed successfully"
            logger.log(f"✅ {result['message']}", Colors.GREEN)

        else:
            # Test should return error (422)
            if response.status_code == 422:
                result["passed"] = True
                result["message"] = "Correctly returned 422 for invalid input"
                logger.log(f"✅ {result['message']}", Colors.GREEN)
            else:
                result["message"] = (
                    f"Expected 422 for invalid input, got {response.status_code}"
                )
                logger.log(f"❌ {result['message']}", Colors.RED)

    except requests.exceptions.ConnectionError:
        result["message"] = f"Connection refused. Is the server running on {BASE_URL}?"
        logger.log(f"❌ {result['message']}", Colors.RED)
        logger.log("   Make sure your FastAPI app is running with: python main.py")
    except requests.exceptions.Timeout:
        result["message"] = (
            "Request timeout (>5 minutes). RAG processing may be too slow."
        )
        logger.log(f"❌ {result['message']}", Colors.RED)
    except Exception as e:
        result["message"] = f"Unexpected error: {str(e)}"
        logger.log(f"❌ {result['message']}", Colors.RED)

    return result


# =============================================================================
# MAIN EXECUTION
# =============================================================================
def main():
    """Run all visible tests and calculate final score"""

    logger.log("=" * 70, Colors.BOLD + Colors.BLUE)
    logger.log(
        "RAG Travel Assistant API (D4) - Visible Test Suite", Colors.BOLD + Colors.BLUE
    )
    logger.log("=" * 70, Colors.BOLD + Colors.BLUE)
    logger.log(
        "\nThis test validates OpenAPI spec compliance and basic RAG functionality.\n"
    )

    # Define test cases
    test_cases = [
        {
            "name": "Test 1: Basic Visa Query",
            "payload": {
                "query": "What are visa requirements for Indians traveling to Japan?"
            },
            "expect_success": True,
        },
        {
            "name": "Test 2: Cultural Information Query",
            "payload": {
                "query": "What are local customs I should know when visiting Thailand?"
            },
            "expect_success": True,
        },
        {
            "name": "Test 3: Missing Field (Should Return 422)",
            "payload": {
                # Missing required 'query' field
            },
            "expect_success": False,
        },
    ]

    # Run all tests and collect results
    results = []
    for tc in test_cases:
        result = run_test(tc["name"], tc["payload"], tc["expect_success"])
        results.append(result)

    # ==========================================================================
    # CALCULATE FINAL RESULTS
    # ==========================================================================
    tests_passed = sum(1 for r in results if r["passed"])

    logger.log(f"\n{'=' * 70}", Colors.BOLD)
    logger.log("FINAL TEST RESULTS", Colors.BOLD + Colors.BLUE)
    logger.log(f"{'=' * 70}", Colors.BOLD)

    for i, (tc, result) in enumerate(zip(test_cases, results), 1):
        status = "✅ PASSED" if result["passed"] else "❌ FAILED"
        color = Colors.GREEN if result["passed"] else Colors.RED
        logger.log(f"Test {i}: {status}", color + Colors.BOLD)
        if not result["passed"]:
            logger.log(f"  Reason: {result['message']}")

    logger.log(f"\nTests Passed: {tests_passed}/{len(test_cases)}")

    if tests_passed == len(test_cases):
        logger.log(
            "🎉 ALL TESTS PASSED! Your API is working correctly.",
            Colors.GREEN + Colors.BOLD,
        )
        logger.log("\n💡 Your API meets the basic requirements. Ready for submission!")
    else:
        logger.log(
            "❌ SOME TESTS FAILED. Please fix the issues before submission.",
            Colors.RED + Colors.BOLD,
        )
        logger.log(
            "\n💡 Check the error messages above and ensure your /rag-travel endpoint"
        )
        logger.log("   follows the OpenAPI specification exactly.")

    logger.log(f"\n{'=' * 70}")

    # Exit with appropriate code
    sys.exit(0 if tests_passed == len(test_cases) else 1)


if __name__ == "__main__":
    main()
