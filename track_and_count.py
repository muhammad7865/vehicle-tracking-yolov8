import cv2 as cv
import numpy as np
import os


# ---------------- TRACK CLASS ----------------
class Track:
    def __init__(self, track_id, cx, cy, bottom_y, frame_id):
        self.id = track_id
        self.cx = cx
        self.cy = cy
        self.bottom_y = bottom_y
        self.prev_bottom_y = bottom_y  # ✅ ADD
        self.last_frame = frame_id
        self.counted = False


# ---------------- VIDEO SETUP ----------------
video_path = "traffic.mp4"
if not os.path.exists(video_path):
    print(f"ERROR: Video file '{video_path}' not found!")
    exit(1)

Video = cv.VideoCapture(video_path)
if not Video.isOpened():
    print("ERROR: Could not open video!")
    exit(1)

fps = int(Video.get(cv.CAP_PROP_FPS))
width = int(Video.get(cv.CAP_PROP_FRAME_WIDTH))
height = int(Video.get(cv.CAP_PROP_FRAME_HEIGHT))
total_frames = int(Video.get(cv.CAP_PROP_FRAME_COUNT))

os.makedirs("runs/track", exist_ok=True)
output_path = "runs/track/yolo_output.mp4"
frames_dir = "runs/track/frames"
os.makedirs(frames_dir, exist_ok=True)

out = cv.VideoWriter(output_path, cv.VideoWriter_fourcc(*"mp4v"), fps, (width, height))

if not out.isOpened():
    print("ERROR: Could not create output video!")
    exit(1)

print(f"Processing video: {video_path}")
print(f"Output will be saved to: {output_path}")
print(f"Video properties: {width}x{height} @ {fps} fps\n")

# ---------------- DETECTOR & PARAMS ----------------
fgbg = cv.createBackgroundSubtractorMOG2(
    history=500, varThreshold=70, detectShadows=False
)

kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (5, 5))

ground_truth = 1
frame_id = 0
vehicleCount = 0

# detection line – your screenshots use y=300
y_line = 300
offset = 25  # vertical band around the line

# heavy-truck size filter (LOOSENED so trucks definitely pass)
MIN_AREA = 18000  # if still 0, try 15000
MIN_W = 160
MIN_H = 90
MIN_AR = 1.2  # width / height
MAX_AR = 5.5

# tracking params
tracks = []
next_track_id = 1
MAX_DIST = 80  # max pixels to associate to existing track
MAX_MISSED_FRAMES = 25  # drop track if unseen for this many frames

# ---------------- MAIN LOOP ----------------
while True:
    isTrue, frame = Video.read()
    if not isTrue:
        break

    frame_id += 1
    if frame_id % 60 == 0 or frame_id == 1:
        print(
            f"Frame {frame_id}/{total_frames} | Heavy vehicles counted: {vehicleCount}"
        )

    # ---- foreground mask ----
    fgmask = fgbg.apply(frame)
    _, fgmask = cv.threshold(fgmask, 200, 255, cv.THRESH_BINARY)
    fgmask = cv.morphologyEx(fgmask, cv.MORPH_CLOSE, kernel, iterations=2)
    fgmask = cv.morphologyEx(fgmask, cv.MORPH_OPEN, kernel, iterations=1)
    fgmask = cv.dilate(fgmask, kernel, iterations=2)

    contours, _ = cv.findContours(fgmask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    detections = []  # (x, y, w, h, cx, cy, bottom_y)

    for cnt in contours:
        area = cv.contourArea(cnt)
        if area < MIN_AREA:
            continue

        x, y, w, h = cv.boundingRect(cnt)
        if w < MIN_W or h < MIN_H:
            continue

        ar = w / float(h)
        if not (MIN_AR <= ar <= MAX_AR):
            continue

        cx = x + w // 2
        cy = y + h // 2
        bottom_y = y + h
        detections.append((x, y, w, h, cx, cy, bottom_y))

    # ---- associate detections with existing tracks ----
    updated_ids = set()

    for x, y, w, h, cx, cy, bottom_y in detections:
        best_track = None
        best_dist = float("inf")

        for track in tracks:
            if frame_id - track.last_frame > MAX_MISSED_FRAMES:
                continue
            dist = np.hypot(cx - track.cx, cy - track.cy)
            if dist < best_dist and dist < MAX_DIST:
                best_dist = dist
                best_track = track

        if best_track is None:
            # create new track
            track = Track(next_track_id, cx, cy, bottom_y, frame_id)
            tracks.append(track)
            next_track_id += 1
            updated_ids.add(track.id)

        else:
            # ✅ update existing track
            best_track.prev_bottom_y = best_track.bottom_y
            best_track.cx = cx
            best_track.cy = cy
            best_track.bottom_y = bottom_y
            best_track.last_frame = frame_id
            updated_ids.add(best_track.id)

            # ✅ COUNTING LOGIC — ONLY HERE
            if not best_track.counted:
                if best_track.prev_bottom_y < y_line and best_track.bottom_y >= y_line:
                    vehicleCount += 1
                    best_track.counted = True
                    print(f"  ✓ Heavy Truck #{vehicleCount} at frame {frame_id}")

        # draw heavy-vehicle box
        cv.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv.putText(
            frame,
            "Heavy Vehicle",
            (x, y - 10),
            cv.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2,
        )

    # drop old tracks
    tracks = [t for t in tracks if frame_id - t.last_frame <= MAX_MISSED_FRAMES]

    # overlays
    cv.line(frame, (0, y_line), (width, y_line), (0, 255, 0), 2)
    cv.putText(
        frame,
        f"Total Vehicles: {vehicleCount}",
        (10, 30),
        cv.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2,
    )
    cv.putText(
        frame,
        f"Frame: {frame_id}/{total_frames}",
        (10, 70),
        cv.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255, 255, 255),
        2,
    )
    cv.putText(
        frame,
        f"Detection Line (y={y_line})",
        (10, height - 20),
        cv.FONT_HERSHEY_SIMPLEX,
        0.6,
        (255, 165, 0),
        1,
    )

    if frame_id % 10 == 0:
        frame_file = os.path.join(frames_dir, f"frame_{frame_id:04d}.jpg")
        cv.imwrite(frame_file, frame)

    out.write(frame)

Video.release()
out.release()

print(f"\nProcessing complete! Processed {frame_id} frames.")
print("\n" + "=" * 50)
print(f"Total Heavy Vehicle Count: {vehicleCount}")
print(f"Ground Truth Count: {ground_truth}")

error = abs(vehicleCount - ground_truth) / ground_truth * 100
print(f"Error Percentage: {error:.2f}%")

accuracy = (
    (1 - abs(vehicleCount - ground_truth) / ground_truth) * 100
    if ground_truth > 0
    else 0
)
print(f"Accuracy: {accuracy:.2f}%")

print(f"\n✓ Output video saved to: {output_path}")
print(f"✓ Sample frames saved to: {frames_dir}")
