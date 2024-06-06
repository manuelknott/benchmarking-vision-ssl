import torch

from models.util import load_checkpoint, initialize_backbone, prepare_state_dict

checkpoints = {
    "resnet50": {
        "url": "https://dl.fbaipublicfiles.com/vissl/model_zoo/pirl_jigsaw_4node_pirl_jigsaw_4node_resnet_22_07_20.34377f59/model_final_checkpoint_phase799.torch",
        "filename": "pirl_resnet50.torch",
    }
}


def load_model(arch: str, **kwargs):
    assert arch in checkpoints.keys(), f"Invalid arch: {arch}"
    model = initialize_backbone(arch, **kwargs)
    ckpt = load_checkpoint(**checkpoints[arch])["classy_state_dict"]["base_model"]["model"]["trunk"]
    ckpt = prepare_state_dict(ckpt, remove_prefix="_feature_blocks.", delete_prefixes=["projection_head.", "prototypes."])
    model.load_state_dict(ckpt)
    return model


if __name__ == '__main__':
    for arch in checkpoints.keys():
        model = load_model(arch=arch)
        print(model)
        out = model(torch.randn(1, 3, 224, 224))
        print(out.shape)
