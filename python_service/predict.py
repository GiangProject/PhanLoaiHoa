# -*- coding: utf-8 -*-
import sys
import json
import torch
import torchvision.transforms as transforms
from PIL import Image
import torchvision.models as models

# --- CÁC THAM SỐ CỐ ĐỊNH ---
# Sử dụng đường dẫn tương đối để file hoạt động ở mọi nơi
MODEL_PATH = 'python_service/models/exp_vit.pth' # <-- SỬA ĐỔI 1: Tên file model ViT
CLASS_MAPPING_PATH = 'python_service/cat_to_name.json'
INPUT_SIZE = 224
IMAGENET_MEAN = [0.485, 0.456, 0.406]
IMAGENET_STD = [0.229, 0.224, 0.225]
DEVICE = torch.device("cpu") # Luôn dùng CPU

# --- HÀM TẢI MODEL VÀ MAPPING (CHẠY 1 LẦN) ---
def build_model_vit(num_classes=102): # <-- SỬA ĐỔI 2: Đổi tên hàm
    """Xây dựng lại cấu trúc model ViT-B/16."""
    # SỬA ĐỔI 3: Sử dụng đúng kiến trúc ViT và classifier head
    model = models.vit_b_16(weights=None)
    num_ftrs = model.heads.head.in_features
    model.heads.head = torch.nn.Linear(in_features=num_ftrs, out_features=num_classes)
    return model

# Tải model
try:
    model = build_model_vit().to(DEVICE) # <-- SỬA ĐỔI 4: Gọi đúng hàm build_model_vit
    model.load_state_dict(torch.load(MODEL_PATH, map_location=DEVICE))
    model.eval()
except Exception as e:
    print(json.dumps({"status": "error", "message": f"Lỗi tải model: {e}"}), file=sys.stderr)
    sys.exit(1)


# Tải mapping tên hoa (Giữ nguyên)
try:
    with open(CLASS_MAPPING_PATH, 'r') as f:
        cat_to_name = json.load(f)
    class_names = [cat_to_name[str(i)] for i in range(1, 103)]
except Exception as e:
    print(json.dumps({"status": "error", "message": f"Lỗi tải file mapping: {e}"}), file=sys.stderr)
    sys.exit(1)


# --- HÀM DỰ ĐOÁN CHÍNH (Giữ nguyên) ---
def predict_flower(image_path, top_k=3):
    """
    Hàm nhận đường dẫn ảnh, tiền xử lý và trả về top K dự đoán.
    """
    try:
        pil_img = Image.open(image_path).convert('RGB')
        
        preprocess = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(INPUT_SIZE),
            transforms.ToTensor(),
            transforms.Normalize(IMAGENET_MEAN, IMAGENET_STD)
        ])
        input_tensor = preprocess(pil_img).unsqueeze(0).to(DEVICE)

        with torch.no_grad():
            output = model(input_tensor)
            probs = torch.nn.functional.softmax(output, dim=1)
        
        top_probs, top_indices = torch.topk(probs, top_k)
        
        top_probs = top_probs.squeeze().cpu().numpy()
        top_indices = top_indices.squeeze().cpu().numpy()
        
        results = []
        if top_k == 1:
            top_indices = [top_indices.item()]
            top_probs = [top_probs.item()]

        for i in range(len(top_indices)):
            label = class_names[top_indices[i]]
            prob = top_probs[i]
            results.append({"label": label, "probability": f"{prob*100:.2f}%"})
            
        return results
    except Exception as e:
        return {"status": "error", "message": f"Lỗi xử lý ảnh: {e}"}


# --- PHẦN THỰC THI KHI ĐƯỢC GỌI TỪ NODE.JS (Giữ nguyên) ---
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(json.dumps({"status": "error", "message": "Sử dụng sai: python predict.py <đường_dẫn_ảnh>"}), file=sys.stderr)
        sys.exit(1)
    
    image_path_from_nodejs = sys.argv[1]
    predictions = predict_flower(image_path_from_nodejs, top_k=3)
    final_result = { "status": "success", "predictions": predictions }
    print(json.dumps(final_result, indent=4))