import os
from pathlib import Path

from feast import FeatureStore, FeatureService
from feast.constants import FEAST_USAGE
from fastapi import FastAPI


os.environ[FEAST_USAGE] = "False"

app = FastAPI()

fs = FeatureStore(repo_path=Path(__file__).parent.parent / "registry")

feast_feature_service: FeatureService = None
feast_entity_rows: dict = None


def _get_feature_service(feature_service: str):
    """Existing feature services:
    feature_service_0 -  50 features
    feature_service_1 - 100 features
    feature_service_2 - 150 features
    feature_service_3 - 200 features
    feature_service_4 - 250 features
    """
    global feast_feature_service
    if feast_feature_service is None or feast_feature_service.name != feature_service:
        feast_feature_service = fs.get_feature_service(feature_service)
    return feast_feature_service


def _get_entity_rows(batch_size: int):
    """Batch size between 1 and 10000"""
    global feast_entity_rows
    if feast_entity_rows is None or len(feast_entity_rows) != batch_size:
        feast_entity_rows = [{"entity": i} for i in range(1, batch_size+1)]
    return feast_entity_rows


@app.get("/get_online_features")
async def get_online_features(feature_service: str = "feature_service_1", batch_size: int = 1):
    """
    To request different feature services and batch sizes, you can use this syntax:
    curl "http://localhost:8000/get_online_features?feature_service_2&batch_size=10"
    """
    features = fs.get_online_features(
        features=_get_feature_service(feature_service),
        entity_rows=_get_entity_rows(batch_size)
    )
    return features.to_dict()


@app.get("/get_online_features_async")
async def get_online_features_async(feature_service: str = "feature_service_1", batch_size: int = 1):
    """
    To request different feature services and batch sizes, you can use this syntax:
    curl "http://localhost:8000/get_online_features_async?feature_service_2&batch_size=10"
    """
    features = await fs.get_online_features_async(
        features=_get_feature_service(feature_service),
        entity_rows=_get_entity_rows(batch_size)
    )
    return features.to_dict()
