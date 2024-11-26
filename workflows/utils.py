import os


def set_hugging_face_hub_token():
    from google.colab import userdata

    hf_hub_token = userdata.get("HUGGING_FACE_HUB_TOKEN")
    assert hf_hub_token, "missing Google colab secret HUGGING_FACE_HUB_TOKEN"

    os.environ["HUGGING_FACE_HUB_TOKEN"] = hf_hub_token
