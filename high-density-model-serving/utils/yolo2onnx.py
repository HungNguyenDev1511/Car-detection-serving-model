import numpy as np
from PIL import Image
from plot import plot_bboxes
from ultralytics import YOLO


IMAGE_PATH = "images/car_2.jpg"
DRAWED_PATH = "images/output.jpg"
MODEL_OUTPUT_PATH = "weights"


def main():
    
    model = YOLO("utils/best.pt")

    # Get predictions
    results = model(source=IMAGE_PATH)

    # Export model
    # We set dynamic to enable dynamic batching,
    # and simplify to infer the whole computation graph
    # and replace redundant ops with constans (constant folding)
    # path = model.export(
    #     format="onnx", opset=14, # Use half=True will be conflict
    #     simplify=True, dynamic=True 
    # )
    # print(f"Model has been exported to {path}")

    # Plot the results
    #import pdb;pdb.set_trace()
    image = Image.open(IMAGE_PATH)
    image = np.asarray(image)
    plot_bboxes(
        image,
        results[0].boxes.data,
        score=False,
        conf=0.75,
        output_path=DRAWED_PATH,
    )


if __name__ == "__main__":
    main()
