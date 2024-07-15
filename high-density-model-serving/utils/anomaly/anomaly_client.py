import json

import requests

if __name__ == "__main__":
    # Define YOUR OWN authservice_session for authentication
    cookies = {
        "authservice_session": "MTcwMDQ1MDE2N3xOd3dBTkZCU1VFRkpTRkZYVVRVMlJWZEhURTlCVmxGT1ZsWkpNa1ZWTjFkWk5FaExUMGxVUms5T1VWSlBVRXRGTWxSVFJUYzNVbEU9fOqjk0noXedW5ccyRtHZ8oaX6UZFzWCXe-y58ojTP-KL",
    }

    # We will send requests with content-type is json
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
    }

    # Define our data for prediction
    data = {
        "inputs": [
            {
                "name": "predict",
                "shape": [1, 18],
                "datatype": "FP32",
                "data": [
                    5.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    1.0,
                    0.0,
                    0.0,
                    255.0,
                    250.0,
                    0.98,
                    0.01,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                ],
            }
        ]
    }

    response = requests.post(
        "http://localhost:8008/v2/models/intrusion-detection/infer",
        cookies=cookies,
        data=json.dumps(data),
        headers=headers,
    )

    print(response.json())