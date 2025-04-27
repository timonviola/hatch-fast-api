"""A simple Fibonacci-API.

The Fibonacci sequence is a sequence in which each element is the sum of the two
elements that precede it. The Fibonacci sequence is numbered from 0. such as:
[0:0, 1:1, 2:1, 3:2, ...]

[Ref](https://en.wikipedia.org/wiki/Fibonacci_sequence)
"""

from typing import Annotated

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field, PositiveInt
from fastapi import APIRouter
from enum import Enum
from functools import cache

# Fibonacci sequence numbers are Int and x <= 0
SequenceNumber = Annotated[int, Field(ge=0)]


class Versions(Enum):
    v1 = "/api/v1"


assert __doc__ is not None
_summary, _description = __doc__.split("\n", 1)[:]
app = FastAPI(title="Fibonacci-api", summary=_summary, description=_description)

API_VERSION_1 = "/api/v1"
router_v1 = APIRouter(prefix=Versions.v1.value, tags=[Versions.v1])

SEQUENCE_NUMBER_BLOCK_LIST: set[SequenceNumber] = set()


@cache
def calculate_fibonacci(n: SequenceNumber) -> SequenceNumber:
    """Calculate the `n`th fibonacci sequence number.

    This function is naively cached.

    Raises:
        ValueError
    """
    match n:
        case 0:
            return 0
        case 1:
            return 1
        case n if n >= 2:
            return calculate_fibonacci(n - 1) + calculate_fibonacci(n - 2)
        case _:
            raise ValueError


async def get_fibonacci(n: SequenceNumber) -> SequenceNumber:
    return calculate_fibonacci(n)


class HealthCheck(BaseModel):
    """Response model to validate and return when performing a health check."""

    status: str = "OK"


@app.get("/")
def read_root():
    return {
        "version": app.version,
        "title": app.title,
        "summary": app.summary,
        "api-versions": {"v1": Versions.v1.value},
        "description": app.description,
    }


@router_v1.get("/fibonacci/{sequence_number}")
async def get_item(sequence_number: SequenceNumber):
    """Return the `n`th Fibonacci number."""
    if sequence_number in SEQUENCE_NUMBER_BLOCK_LIST:
        raise HTTPException(status_code=409, detail="Item on block list.") 
    return await get_fibonacci(sequence_number)


@router_v1.get("/fibonacci_range/{sequence_number}")
async def get_range(
    sequence_number: SequenceNumber,
    limit: PositiveInt = 100,
    page: SequenceNumber = 0,
) -> dict[int, SequenceNumber]:
    """Return the Fibonacci sequence until the `n`th number.

    Returns empty response if pagination/limit is configured out of range.
    """
    return {
        i: await get_fibonacci(i)
        for i in range(page * limit, min(sequence_number, (page + 1) * limit))
        if i not in SEQUENCE_NUMBER_BLOCK_LIST
    }

@router_v1.post("/fibonacci/block/{sequence_number}", status_code=201, tags=["blocklist"])
def add_to_block_list(sequence_number: SequenceNumber) -> set[SequenceNumber]:
    """Add a number to the block list."""
    global SEQUENCE_NUMBER_BLOCK_LIST
    SEQUENCE_NUMBER_BLOCK_LIST |= set([sequence_number])
    return SEQUENCE_NUMBER_BLOCK_LIST

@router_v1.get("/fibonacci/block/", tags=["blocklist"])
def get_block_list() -> set[SequenceNumber]:
    """Show the block list."""
    return SEQUENCE_NUMBER_BLOCK_LIST

@router_v1.delete("/fibonacci/block/{sequence_number}", tags=["blocklist"])
def remove_from_block_list(sequence_number: SequenceNumber) -> set[SequenceNumber]:
    """Drop single item from drop list."""
    global SEQUENCE_NUMBER_BLOCK_LIST
    try:
        SEQUENCE_NUMBER_BLOCK_LIST.remove(sequence_number)
    except KeyError:
        # Number was not part of the list.
        pass
    return SEQUENCE_NUMBER_BLOCK_LIST

@router_v1.delete("/fibonacci/block/", status_code=204, tags=["blocklist"])
def remove_all_from_block_list():
    """Drop all from block list."""
    global SEQUENCE_NUMBER_BLOCK_LIST
    SEQUENCE_NUMBER_BLOCK_LIST = set()
    return SEQUENCE_NUMBER_BLOCK_LIST

@app.get(
    "/health",
    tags=["healthcheck"],
    summary="Perform a Health Check",
    response_description="Return HTTP Status Code 200 (OK)",
    status_code=status.HTTP_200_OK,
    response_model=HealthCheck,
)
def get_health() -> HealthCheck:
    """
    ## Perform a Health Check
    Endpoint to perform a healthcheck on. This endpoint can primarily be used Docker
    to ensure a robust container orchestration and management is in place. Other
    services which rely on proper functioning of the API service will not deploy if this
    endpoint returns any other HTTP status code except 200 (OK).
    Returns:
        HealthCheck: Returns a JSON response with the health status
    """
    return HealthCheck(status="OK")


app.include_router(router_v1)
