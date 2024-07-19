import numpy as np
import cv2
import tensorrt as trt
import common
from process import draw_image, postprocess, preprocess

# Still, define some constants
IMAGE_PATH = "images/bus.jpg"
DRAWED_PATH = "images/tensorrt_output.jpg"

ONNX_FILE_PATH = "model_repo/yolov8n/1/model.onnx"
ENGINE_FILE_PATH = "model_repo/yolov8n-tensorrt/1/model.engine"

INPUT_SHAPE = (640, 640)  # height, width
OUTPUT_SHAPE = (84, 8400)

TRT_LOGGER = trt.Logger(trt.Logger.WARNING)

def load_engine(engine_file_path):
    print("Reading engine from file {}".format(engine_file_path))
    with open(engine_file_path, "rb") as f, trt.Runtime(TRT_LOGGER) as runtime:
        return runtime.deserialize_cuda_engine(f.read())

def main():
    # Create a logger is a must before create a builder
    builder = trt.Builder(TRT_LOGGER)

    # Create a network definition
    EXPLICIT_BATCH = 1 << (int)(trt.NetworkDefinitionCreationFlag.EXPLICIT_BATCH)
    network = builder.create_network(EXPLICIT_BATCH)

    # Import a model using ONNX Parser
    # and populate ONNX to our network definition
    parser = trt.OnnxParser(network, TRT_LOGGER)
    success = parser.parse_from_file(ONNX_FILE_PATH)
    # Print all errors if any
    for idx in range(parser.num_errors):
        print(parser.get_error(idx))
    if not success:
        raise ValueError("Failed to populate network from ONNX file!")

    # Create a build config to specify how TensorRT should
    # optimize the model, for example memory limit, then build
    # the engine, please refer to this documentation https://onnxruntime.ai/docs/execution-providers/TensorRT-ExecutionProvider.html#execution-provider-options
    config = builder.create_builder_config()
    network.get_input(0).shape = [1, 3, INPUT_SHAPE[0], INPUT_SHAPE[1]]
    serialized_engine = builder.build_serialized_network(network, config)
    with open(ENGINE_FILE_PATH, "wb") as f:
        f.write(serialized_engine)
    print(f"Model has been exported to {ENGINE_FILE_PATH}")

    # Now, load the engine from file
    print(f"Building an engine from file {ENGINE_FILE_PATH}")
    runtime = trt.Runtime(TRT_LOGGER)
    with open(ENGINE_FILE_PATH, "rb") as f:
        serialized_engine = f.read()
    engine = runtime.deserialize_cuda_engine(serialized_engine)

    # Do inference with TensorRT
    image = cv2.imread(IMAGE_PATH)
    resized = preprocess(image, INPUT_SHAPE).astype(np.float32)
    
    trt_outputs = []
    with engine.create_execution_context() as context:
        inputs, outputs, bindings, stream = common.allocate_buffers(engine)
        # Do inference
        print("Running inference on image {}...".format(IMAGE_PATH))
        # Set host input to the image. The common.do_inference function will copy the input to the GPU before executing.
        inputs[0].host = resized
        trt_outputs = common.do_inference_v2(context, bindings=bindings, inputs=inputs, outputs=outputs, stream=stream)
        
    trt_outputs = trt_outputs[0].reshape(OUTPUT_SHAPE)

    # Plot the results
    bboxes, scores, class_ids = postprocess(trt_outputs, image.shape)
    draw_image(image, bboxes, scores, class_ids, DRAWED_PATH)


if __name__ == "__main__":
    main()
