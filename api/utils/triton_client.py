import requests
import json
import numpy as np
import wget
import os
import cv2
from classes import CLASSES  # Import danh sách CLASSES từ file classes.py


def preprocess(cv2_image, model_shape=(640, 640)):
    image_rgb = cv2.cvtColor(cv2_image, cv2.COLOR_BGR2RGB)
    resized = cv2.resize(image_rgb, model_shape)

    # Scale input pixel value to 0 to 1
    input_image = resized / 255.0
    input_image = input_image.transpose(2, 0, 1)
    result = input_image[np.newaxis, :, :, :].astype(np.float32)

    return result


def xywh2xyxy(x):
    # Convert bounding box (x, y, w, h) to bounding box (x1, y1, x2, y2)
    y = np.copy(x)
    y[..., 0] = x[..., 0] - x[..., 2] / 2
    y[..., 1] = x[..., 1] - x[..., 3] / 2
    y[..., 2] = x[..., 0] + x[..., 2] / 2
    y[..., 3] = x[..., 1] + x[..., 3] / 2
    return y


def nms(boxes, scores, iou_threshold):
    # Sort by score
    sorted_indices = np.argsort(scores)[::-1]

    keep_boxes = []
    while sorted_indices.size > 0:
        # Pick the last box
        box_id = sorted_indices[0]
        keep_boxes.append(box_id)

        # Compute IoU of the picked box with the rest
        ious = compute_iou(boxes[box_id, :], boxes[sorted_indices[1:], :])

        # Remove boxes with IoU over the threshold
        keep_indices = np.where(ious < iou_threshold)[0]

        sorted_indices = sorted_indices[keep_indices + 1]

    return keep_boxes


def compute_iou(box, boxes):
    # Compute xmin, ymin, xmax, ymax for both boxes
    xmin = np.maximum(box[0], boxes[:, 0])
    ymin = np.maximum(box[1], boxes[:, 1])
    xmax = np.minimum(box[2], boxes[:, 2])
    ymax = np.minimum(box[3], boxes[:, 3])

    # Compute intersection area
    intersection_area = np.maximum(0, xmax - xmin) * np.maximum(0, ymax - ymin)

    # Compute union area
    box_area = (box[2] - box[0]) * (box[3] - box[1])
    boxes_area = (boxes[:, 2] - boxes[:, 0]) * (boxes[:, 3] - boxes[:, 1])
    union_area = box_area + boxes_area - intersection_area

    # Compute IoU
    iou = intersection_area / union_area

    return iou


def postprocess(outputs, original_shape, model_shape=(640, 640), threshold=0.8):
    model_height, model_width = model_shape
    original_height, original_width = original_shape[:2]
    outputs = np.array(outputs[0]["data"]).reshape(outputs[0]["shape"])
    predictions = np.squeeze(outputs).T

    # Filter out object confidence scores below threshold
    scores = np.max(predictions[:, 4:], axis=1)
    predictions = predictions[scores > threshold, :]
    scores = scores[scores > threshold]
    class_ids = np.argmax(predictions[:, 4:], axis=1)

    # Get bounding boxes for each object
    bboxes = predictions[:, :4]

    # Rescale bboxes
    model_shape = np.array([model_width, model_height, model_width, model_height])
    original_shape = np.array(
        [original_width, original_height, original_width, original_height]
    )
    bboxes = np.divide(bboxes, model_shape, dtype=np.float32)
    bboxes *= original_shape
    bboxes = bboxes.astype(np.int32)

    # Apply non-maxima suppression to suppress weak, overlapping bounding boxes
    indices = nms(bboxes, scores, 0.3)

    return bboxes[indices], scores[indices], class_ids[indices]


def draw_image(image, bboxes, scores, class_ids):
    image_draw = image.copy()
    for bbox, score, label in zip(xywh2xyxy(bboxes), scores, class_ids):
        bbox = bbox.round().astype(np.int32).tolist()
        cls_id = int(label)
        cls = CLASSES[cls_id]
        color = (0, 255, 0)
        cv2.rectangle(image_draw, tuple(bbox[:2]), tuple(bbox[2:]), color, 2)
        cv2.putText(
            image_draw,
            f"{cls}:{int(score*100)}",
            (bbox[0], bbox[1] - 2),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.60,
            [225, 255, 255],
            thickness=1,
        )
        cv2.imwrite("drawed.jpg", image_draw)


def main():
    image_url = "https://ultralytics.com/images/bus.jpg"
    image_name = os.path.basename(image_url)
    if not os.path.exists(image_name):
        wget.download(image_url)

    original_image = cv2.imread(image_name)
    image = preprocess(original_image)

    request_data = {
        "inputs": [
            {
                "name": "images",
                "shape": image.shape,
                "datatype": "FP32",
                "data": image.flatten().tolist(),  # Flatten the image and convert to list
            }
        ]
    }

    headers = {
        "Content-Type": "application/json",  # Change content type to JSON
    }

    response = requests.post(
        "http://localhost:8008/v2/models/onnx/infer",
        headers=headers,
        data=json.dumps(request_data),
        verify=False,
    ).json()

    result = response["outputs"]
    bboxes, scores, class_ids = postprocess(result, original_image.shape)
    print(bboxes)
    print(scores)
    print(class_ids)
    draw_image(
        original_image, bboxes, scores, class_ids
    )  # Use DRAWED_PATH instead of "drawed.jpg"


if __name__ == "__main__":
    main()
