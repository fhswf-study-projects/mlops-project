from fastapi import APIRouter

router = APIRouter(
    prefix="/api", tags=["PredictionMaker"]
)


@router.get("/test")
def test_endpoint():
    return {"content": "API's functioning"}


@router.get("/async-test")
def test_async_endpoint():
    return {"content": "API's functioning in async way"}