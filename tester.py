import torch
from lime_3d.lime_3d import VideoPerturbationAnalyzer
from torchvision.models.video import swin3d_t, Swin3D_T_Weights
import torchvision.transforms as transforms
import numpy as np

rows, cols = 3, 3
num_matrix = 10
video_path = r'videos\riding.mp4'
desired_action = 274

def tranform_frames(frames):
    frames = np.array(frames)
    
    # Transform the video frames
    transform = transforms.Compose([
        transforms.ToPILImage(),
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5]),
    ])
    
    frames = [transform(frame) for frame in frames]
    frames = torch.stack(frames)
    
    # Reshape to (B, C, T, H, W) format
    frames = frames.permute(1, 0, 2, 3).unsqueeze(0)
    return frames

def predict_fn(video):
    with torch.no_grad():
        outputs = model(video)
    return torch.nn.functional.softmax(outputs, dim=1).cpu().numpy()

# Load the pretrained model
model = swin3d_t(weights=Swin3D_T_Weights.DEFAULT)
model.eval()

# Example usage:
analyzer = VideoPerturbationAnalyzer('out_video.mp4', num_matrix, rows, cols)
analyzer.explain_instance(model_function=predict_fn,
                          tranform_frames_function=tranform_frames,
                          desired_action=desired_action,
                          video_path=video_path)
