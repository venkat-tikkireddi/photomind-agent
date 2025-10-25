import cv2
from insightface.app import FaceAnalysis
import os

# Initialize the InsightFace model (download on first run)
face_app = FaceAnalysis()
face_app.prepare(ctx_id=0, det_size=(640, 640))  # Use GPU (ctx_id=0) if available

def extract_faces(photo_list):
    results = []
    for photo in photo_list:
        img = cv2.imread(photo["path"])
        faces = face_app.get(img)
        # Each 'face' object has embedding, bbox, etc.
        for face in faces:
            results.append({
                "photo_path": photo["path"],
                "bbox": face.bbox.tolist(),
                "embedding": face.embedding.tolist()
            })
    return results

if __name__ == "__main__":
    import json
    # Load metadata output from previous step
    with open("photo_meta.json", "r") as f:
        photo_list = json.load(f)
    face_meta = extract_faces(photo_list)
    print(f"Extracted {len(face_meta)} faces.")
    # Save results for later modules
    with open("face_meta.json", "w") as f:
        json.dump(face_meta, f)
