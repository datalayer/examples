FROM datalayer/jupyter-kernel-python:0.0.6

USER root

RUN apt-get update && \
    apt-get install -y libgl1-mesa-glx libglib2.0-0 wget git && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

ENV RAY_DEDUP_LOGS=0

ARG FACE_CASCADE_FN="haarcascade_frontalface_default.xml"

RUN wget "https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades/${FACE_CASCADE_FN}" -P /tmp

ENV MODEL_PATH="/tmp/${FACE_CASCADE_FN}"

RUN pip install \
  "pytube @ git+https://github.com/modal-labs/pytube" \
  opencv-python~=4.7.0.72 \
  moviepy~=1.0.3

RUN pip install ray_ease

USER ${NB_UID}
