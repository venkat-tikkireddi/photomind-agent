import torch
from PIL import Image
import clip

device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)

def get_clip_tags(photo_list, candidate_events):
    results = []
    for photo in photo_list:
        image = preprocess(Image.open(photo["path"])).unsqueeze(0).to(device)
        text = clip.tokenize(candidate_events).to(device)
        with torch.no_grad():
            image_features = model.encode_image(image)
            text_features = model.encode_text(text)
            # Cosine similarity
            scores = (image_features @ text_features.T).squeeze(0).cpu().numpy()
            best_idx = scores.argmax()
            results.append({
                "photo_path": photo["path"],
                "event_tag": candidate_events[best_idx],
                "score": float(scores[best_idx])
            })
    return results

if __name__ == "__main__":
    import json
    candidate_events = ["wedding", "birthday", "vacation", "family", "friends"]
    with open("photo_meta.json", "r") as f:
        photo_list = json.load(f)
    tags = get_clip_tags(photo_list, candidate_events)
    with open("event_tags.json", "w") as f:
        json.dump(tags, f)
