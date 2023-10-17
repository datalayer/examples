FROM python:3.10-slim-bullseye

RUN apt-get update \
    && apt-get install -y libgl1-mesa-glx \
    libglib2.0-0 \
    wget \
    git

ARG FN_CONFIG="haarcascade_frontalface_default.xml"
ENV FACE_CASCADE_FN=${FN_CONFIG}

RUN wget "https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades/${FACE_CASCADE_FN}" -P /root

RUN pip install "pytube @ git+https://github.com/modal-labs/pytube" \
    opencv-python~=4.7.0.72 \
    moviepy~=1.0.3 \
    ray_ease \
    ipykernel \
    ipywidgets