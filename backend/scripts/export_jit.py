import os
import json
import torch
from app.services.ml_service import TransformerRec

def export_transformer_to_jit():
    print("Starting TorchScript JIT compiler for TransformerRec...")
    assets_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "models"))
    
    # Load vocab
    vocab_path = os.path.join(assets_dir, "encoder", "vocab.json")
    with open(vocab_path, "r", encoding="utf-8") as f:
        vocab = json.load(f)
    
    # Initialize PyTorch model
    model = TransformerRec(vocab_size=len(vocab))
    model_path = os.path.join(assets_dir, "encoder", "gym_bert_v2_ep27_hit0.3522.pth")
    model.load_state_dict(torch.load(model_path, map_location=torch.device("cpu")))
    model.eval()
    
    # Dummy input for tracing (batch_size=1, seq_len=15)
    dummy_input = torch.randint(0, len(vocab), (1, 15), dtype=torch.long)
    
    # Export path
    jit_path = os.path.join(assets_dir, "encoder", "transformer_jit.pt")
    
    # Compile to TorchScript (JIT)
    with torch.no_grad():
        traced_model = torch.jit.trace(model, dummy_input)
        
    # Optimize for Inference
    traced_model = torch.jit.optimize_for_inference(traced_model)
    
    traced_model.save(jit_path)
    print(f"Success! Model compiled for LibTorch/Triton and saved to: {jit_path}")

if __name__ == "__main__":
    export_transformer_to_jit()
