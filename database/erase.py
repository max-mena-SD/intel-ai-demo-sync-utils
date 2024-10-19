data = (
    "3dsegmentationpointclouds",
    "3D-segmentation-point-clouds",
    "/openvinotoolkit/openvino_notebooks/tree/latest/notebooks/3D-segmentation-point-clouds",
    '# Part Segmentation of 3D Point Clouds with OpenVINO™\n\n[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/eaidova/openvino_notebooks_binder.git/main?urlpath=git-pull%3Frepo%3Dhttps%253A%252F%252Fgithub.com%252Fopenvinotoolkit%252Fopenvino_notebooks%26urlpath%3Dtree%252Fopenvino_notebooks%252Fnotebooks%2F3D-segmentation-point-clouds%2F3D-segmentation-point-clouds.ipynb)\n[![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/openvinotoolkit/openvino_notebooks/blob/latest/notebooks/3D-segmentation-point-clouds/3D-segmentation-point-clouds.ipynb)\n\n<p align="center">\n    <img src="https://user-images.githubusercontent.com/91237924/185752178-3882902c-907b-4614-b0e6-ea1de08bf3ef.png"/>\n</p>\n\nPoint clouds are an important type of geometric data structure. OpenVINO can directly consume point cloud data and perform inference with it.\n\n## Notebook Contents\n\nThis notebook demonstrates how to process [point cloud](https://en.wikipedia.org/wiki/Point_cloud) data and run 3D Part Segmentation with OpenVINO. The inputs of this task are a collection of individual data points in a three-dimensional plane with each point having a set coordinates on the X, Y, and Z axes.\n\nThis notebook uses a pre-trained [PointNet](https://arxiv.org/abs/1612.00593) model to detect each part of a chair and return its category.\n\n\n## Installation Instructions\n\nThis is a self-contained example that relies solely on its own code.</br>\nWe recommend running the notebook in a virtual environment. You only need a Jupyter server to start.\nFor details, please refer to [Installation Guide](../../README.md).\n\n<img referrerpolicy="no-referrer-when-downgrade" src="https://static.scarf.sh/a.png?x-pxid=5b5a4db0-7875-4bfb-bdbd-01698b5b1a77&file=notebooks/3D-segmentation-point-clouds/README.md" />\n',
    "OpenVINO",
    "This notebook demonstrates how to process [point cloud] data and run 3D Part Segmentation with OpenVINO. The inputs of this task are a collection of individual data points in a three-dimensional plane with each point having a set coordinates on the X, Y and Z axes.",
    "2024-10-10",
)


otro = {
    "industry": {"labels": ["Entertainment", "Cybersecurity", "Retail"]},
    "type": {
        "labels": ["Anomaly Detection", "Computer Vision", "Recommendation Systems"]
    },
    "technology": {"labels": ["Edge Computing", "Machine Learning", "Computer Vision"]},
    "complexity_level": {"labels": ["Advanced", "Beginner", "Expert"]},
    "platform_tools": {"labels": ["OpenVINO", "Keras", "PyTorch"]},
    "use_case_functionality": {
        "labels": [
            "Autonomous Systems",
            "Real-time Video Processing",
            "Recommendation Engine",
        ]
    },
}

otro_mejor = {
    "industry": ["Entertainment", "Retail", "Education"],
    "type": ["Recommendation Systems", "Anomaly Detection", "Computer Vision"],
    "technology": ["Edge Computing", "Machine Learning", "Computer Vision"],
    "complexity_level": ["Advanced", "Beginner", "Expert"],
    "platform_tools": ["Keras", "PyTorch", "OpenVINO"],
    "use_case_functionality": [
        "Autonomous Systems",
        "Recommendation Engine",
        "Real-time Video Processing",
    ],
}
