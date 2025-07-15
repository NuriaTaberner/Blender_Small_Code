import bpy
import os
import re

# === CONFIGURATION ===
directory = r"File_path" #<------------ Add here your image file path -------
keyword = "Select_Keyword" #<---------- Load only images that have this keyword 
frame_pattern = r"(\d+)(?!.*\d)"  # Grab the last numeric group
channel = 2

# === FILE COLLECTION ===
all_files = sorted([
    f for f in os.listdir(directory)
    if keyword in f and f.lower().endswith((".png", ".jpg", ".jpeg"))
])

frame_to_file = {}
for f in all_files:
    match = re.search(frame_pattern, f)
    if match:
        frame = int(match.group(1))
        frame_to_file[frame] = f

# === GROUP CONSECUTIVE FRAMES ===
sorted_frames = sorted(frame_to_file.keys())
sequences = []
current_group = []

for i, frame in enumerate(sorted_frames):
    if i == 0 or frame == sorted_frames[i - 1] + 1:
        current_group.append(frame)
    else:
        sequences.append(current_group)
        current_group = [frame]
if current_group:
    sequences.append(current_group)

# === PREPARE SEQUENCER ===
scene = bpy.context.scene
seq_editor = scene.sequence_editor or scene.sequence_editor_create()

# === CREATE SEQUENCE STRIPS ===
for group in sequences:
    filenames = [frame_to_file[f] for f in group]
    start_frame = group[0]

    strip = seq_editor.sequences.new_image(
        name=f"Sequence_{start_frame}",
        filepath=os.path.join(directory, filenames[0]),
        channel=channel,
        frame_start=start_frame
    )

    # Add remaining frames to the strip
    for fname in filenames[1:]:
        strip.elements.append(fname)

#    channel += 1  # Stack vertically to avoid overlaps

print(f"✅ Added {len(sequences)} image sequences with {len(all_files)} frames.")
