# YouTube Face Detection

This folder presents an example of YouTube face detection, inspired by the original source code available at [Modal Labs GitHub](https://github.com/modal-labs/modal-examples/blob/main/03_scaling_out/youtube_face_detection.py).

It's a Python project that utilizes OpenCV for detecting faces in YouTube videos.

## Docker Image

```bash
export DATALAYER_DOCKER_REPO=datalayer
make build
make push
```

## Local Setup using Conda

If you want to run this code locally, it's essential to set up the required environment.

We recommend using Conda for this purpose. Follow these steps:

1. Clone this repository or download the code to your local machine.
2. Navigate to the project directory using your terminal.
3. Create a custom Conda environment by using the provided `environment.yml` file and activate it:

```bash
conda env create --file environment.yml
conda activate datalayer-example-youtube-face-detection
```

To perform face detection, you need to obtain the Haar Cascade classifier model for frontal face detection. You can download the model from the official OpenCV repository by clicking [here](https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades/haarcascade_frontalface_default.xml).

After downloading the model, place it in the project directory.

Now, your environment is set up, and you have the necessary model for face detection. You are ready to run the YouTube face detection code provided in this repository. Enjoy face detection on YouTube videos!
