#!/usr/bin/env python3
"""Today's Demo: Run roboflow/supervision (today's GitHub trending #7)
on a sample video with YOLO11. Produce a GIF showing object detection
+ annotation in action.
"""
import os
from pathlib import Path

import imageio.v3 as iio
import numpy as np
import supervision as sv
from supervision.assets import VideoAssets, download_assets
from ultralytics import YOLO

ROOT = Path(__file__).resolve().parent.parent
ASSETS_DIR = ROOT / "assets"
ASSETS_DIR.mkdir(exist_ok=True)

VIDEO_PATH = ASSETS_DIR / "people-walking.mp4"
GIF_PATH = ASSETS_DIR / "demo-today.gif"

# Download sample video if not cached
if not VIDEO_PATH.exists():
    print("Downloading sample video...")
    os.chdir(ASSETS_DIR)
    download_assets(VideoAssets.PEOPLE_WALKING)

print("Loading YOLO11n model...")
model = YOLO("yolo11n.pt")

print("Setting up annotators...")
box_annotator = sv.BoxAnnotator(thickness=2)
label_annotator = sv.LabelAnnotator(text_scale=0.5, text_thickness=1)
trace_annotator = sv.TraceAnnotator(thickness=2, trace_length=20)
tracker = sv.ByteTrack()

print(f"Processing video: {VIDEO_PATH}")
frames_iter = sv.get_video_frames_generator(str(VIDEO_PATH))

processed_frames = []
target_w = 480
fps_out = 12
max_frames = 60
stride = 2  # process every 2nd frame

for i, frame in enumerate(frames_iter):
    if i >= max_frames * stride:
        break
    if i % stride != 0:
        continue

    results = model(frame, verbose=False)[0]
    detections = sv.Detections.from_ultralytics(results)
    detections = detections[detections.class_id == 0]  # persons only
    detections = tracker.update_with_detections(detections)

    labels = [f"#{tid} {conf:.2f}" for tid, conf in zip(detections.tracker_id, detections.confidence)]

    annotated = trace_annotator.annotate(scene=frame.copy(), detections=detections)
    annotated = box_annotator.annotate(scene=annotated, detections=detections)
    annotated = label_annotator.annotate(scene=annotated, detections=detections, labels=labels)

    h, w = annotated.shape[:2]
    target_h = int(h * target_w / w)
    annotated = annotated[:, :, ::-1]  # BGR→RGB
    import cv2
    annotated = cv2.resize(annotated, (target_w, target_h), interpolation=cv2.INTER_AREA)
    processed_frames.append(annotated)
    print(f"  frame {len(processed_frames)}/{max_frames}: {len(detections)} persons")

print(f"Saving GIF to {GIF_PATH}...")
iio.imwrite(str(GIF_PATH), processed_frames, fps=fps_out, loop=0)
print(f"Done. Size: {GIF_PATH.stat().st_size / 1024:.1f} KB")
