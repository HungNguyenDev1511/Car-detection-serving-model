# Ref: https://github.com/kserve/modelmesh-serving/blob/release-0.7/docs/runtimes/mlserver_custom.md
from typing import List

from alibi_detect.saving import load_detector
from mlserver import MLModel, types
from mlserver.utils import get_model_uri

from loguru import logger
import os
import numpy as np

class CustomMLModel(MLModel):
    async def load(self) -> bool:
        # get URI to model data
        model_uri = await get_model_uri(
            self._settings
        )
        logger.debug(f"model_uri: {model_uri}")

        # parse/process file and instantiate the model
        if os.path.exists(model_uri):
            self._load_model_from_file(model_uri)
            logger.info("Model loaded successfully!")
            self.ready = True
        else:
            logger.info("Model not found!")
            self.ready = False

        # set ready to signal that model is loaded
        return self.ready

    async def predict(self, payload: types.InferenceRequest) -> types.InferenceResponse:
        return types.InferenceResponse(
            model_name=self.name,
            model_version=self.version,
            outputs=self._predict_outputs(payload),
        )

    def _load_model_from_file(self, file_uri):
        # assume that file_uri is an absolute path
        # TODO: load model from file and instantiate class data
        logger.info("Loading model from file...")
        self.model = load_detector(file_uri)

    def _predict_outputs(
        self, payload: types.InferenceRequest
    ) -> List[types.ResponseOutput]:
        # get inputs from the request
        inputs = payload.inputs
        logger.debug(f"Received a payload with inputs of type {type(inputs)}")
        logger.debug(inputs)
        
        # Extract inputs's data
        for input in inputs:
            pred_data = np.array(input.data)
            logger.debug(f"Data for prediction: {pred_data}")
            break

        outputs = self.model.predict(
            [pred_data],
            return_instance_score=True,
            return_feature_score=False,
        )

        logger.debug(f"Prediction's result: {outputs}")

        return [
            types.ResponseOutput(
                name="anomaly",
                shape=outputs["data"]["is_outlier"].shape,
                datatype="FP32",
                data=outputs["data"]["is_outlier"].tolist()
            )
        ]
