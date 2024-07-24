import os
import xml.etree.ElementTree
import posixpath
import cv2
import numpy

from utils import config


def load_image(file_name, split="train"):
    path = posixpath.join(config.data_dir, config.image_dir, split, file_name + ".jpg")
    image = cv2.imread(path)
    return image


def load_label(file_name, split="train"):
    # Construct the new path for the label file
    path = posixpath.join(config.data_dir, config.label_dir, split, file_name + ".txt")

    boxes = []

    # Read the text file line by line
    with open(path, "r") as f:
        for line in f:
            # Split the line into coordinates
            _, x_min, y_min, x_max, y_max = line.strip().split()
            x_min = float(x_min)
            y_min = float(y_min)
            x_max = float(x_max)
            y_max = float(y_max)

            boxes.append([x_min, y_min, x_max, y_max])

    boxes = numpy.asarray(boxes, numpy.float32)
    return boxes


def resize(image, boxes=None):
    shape = image.shape[:2]
    scale = min(config.image_size / shape[1], config.image_size / shape[0])
    image = cv2.resize(image, (int(scale * shape[1]), int(scale * shape[0])))

    image_padded = numpy.zeros([config.image_size, config.image_size, 3], numpy.uint8)

    dw = (config.image_size - int(scale * shape[1])) // 2
    dh = (config.image_size - int(scale * shape[0])) // 2

    image_padded[
        dh : int(scale * shape[0]) + dh, dw : int(scale * shape[1]) + dw, :
    ] = image.copy()

    if boxes is None:
        return image_padded, scale, dw, dh

    else:
        boxes[:, [0, 2]] = boxes[:, [0, 2]] * scale + dw
        boxes[:, [1, 3]] = boxes[:, [1, 3]] * scale + dh

        return image_padded, boxes


def random_flip(image, boxes):
    if numpy.random.uniform() < 0.5:
        image = cv2.flip(image, 1)
        boxes[:, 0] = image.shape[1] - boxes[:, 2]
        boxes[:, 2] = image.shape[1] - boxes[:, 0]
    return image, boxes


def process_box(boxes):
    anchors_mask = [[6, 7, 8], [3, 4, 5], [0, 1, 2]]
    anchors = config.anchors
    box_centers = (boxes[:, 0:2] + boxes[:, 2:4]) / 2
    box_size = boxes[:, 2:4] - boxes[:, 0:2]

    y_true_1 = numpy.zeros(
        (
            config.image_size // 32,
            config.image_size // 32,
            3,
            5 + len(config.class_dict),
        ),
        numpy.float32,
    )
    y_true_2 = numpy.zeros(
        (
            config.image_size // 16,
            config.image_size // 16,
            3,
            5 + len(config.class_dict),
        ),
        numpy.float32,
    )
    y_true_3 = numpy.zeros(
        (config.image_size // 8, config.image_size // 8, 3, 5 + len(config.class_dict)),
        numpy.float32,
    )

    y_true = [y_true_1, y_true_2, y_true_3]

    box_size = numpy.expand_dims(box_size, 1)

    min_np = numpy.maximum(-box_size / 2, -anchors / 2)
    max_np = numpy.minimum(box_size / 2, anchors / 2)

    whs = max_np - min_np

    overlap = whs[:, :, 0] * whs[:, :, 1]
    union = (
        box_size[:, :, 0] * box_size[:, :, 1]
        + anchors[:, 0] * anchors[:, 1]
        - whs[:, :, 0] * whs[:, :, 1]
        + 1e-10
    )

    iou = overlap / union
    best_match_idx = numpy.argmax(iou, axis=1)

    ratio_dict = {1.0: 8.0, 2.0: 16.0, 3.0: 32.0}
    for i, idx in enumerate(best_match_idx):
        feature_map_group = 2 - idx // 3
        ratio = ratio_dict[numpy.ceil((idx + 1) / 3.0)]
        x = int(numpy.floor(box_centers[i, 0] / ratio))
        y = int(numpy.floor(box_centers[i, 1] / ratio))
        k = anchors_mask[feature_map_group].index(idx)
        # c = labels[i]

        y_true[feature_map_group][y, x, k, :2] = box_centers[i]
        y_true[feature_map_group][y, x, k, 2:4] = box_size[i]
        y_true[feature_map_group][y, x, k, 4] = 1.0
        # y_true[feature_map_group][y, x, k, 5 + c] = 1.

    return y_true_1, y_true_2, y_true_3
