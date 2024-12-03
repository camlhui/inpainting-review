# Image inpainting

## Introduction

> 💡 Inpainting replaces or edits specific areas of an image. This makes it a useful tool for image restoration like removing defects and artifacts, or even replacing an image area with something entirely new. Inpainting relies on a mask to determine which regions of an image to fill in.
*(for more information please check https://huggingface.co/docs/diffusers/using-diffusers/inpaint)*

Recent advances in AI have enabled the generation of high-resolution, realistic images on demand through various guidance techniques such as text prompts and images. These breakthroughs are set to revolutionize industries like e-commerce, fashion, real estate, marketing, and the arts. Essentially, it automates, scales and extends capabilities traditionally provided by tools like Photoshop, unlocking new levels of creativity and efficiency.

In this context we will review here how current available solutions address challenges posed by furniture image editing with a focus on new objects addition to enhance or accessorize existing furniture displays.

## Benchmark dataset

![Benchmark sample](/images/benchmark_grid.png)

> 👀 Prompts are available with the samples in the following [figure](/images/benchmark_full.png)

Our benchmark dataset consists of ten carefully designed samples (image, mask, prompts), selected to evaluate the performance of different solutions across a range of quality and reliability criteria. These include:
- **Realism**, how natural and lifelike the inpainted regions appear.
- **Adaptability**, the ability to adhere to complex and diverse instructions
- **Unmask image preservation**, ensuring the unedited parts of the image remain unaffected.
- **Consistency** with unmasked areas, icluding alignment in lighting, reflections, shadows, style, perspective, and textures.


## Techniques

Image inpainting has been a well-established technique but has seen remarkable progress recently, thanks to advances in Deep Learning and, more specifically, the introduction of Latent Diffusion Models ([High-Resolution Image Synthesis with Latent Diffusion Models](https://arxiv.org/pdf/2112.10752)). These advancements have enabled industry applications for image inpainting, offering capabilities such as mega-pixel resolution, masking, and text-guided generation.

All the models reviewed here belong to the family of latent diffusion models and are summarized below:

| Model                               | Release Date   | Architecture                                                                 | Size  | Max Resolution | Key Characteristics                                                                                                                                                              |
|-------------------------------------|----------------|------------------------------------------------------------------------------|-------|----------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `FLUX.1-Fill-dev-nf4`                 | Nov 24, 2024   | Rectified flow transformer                           | 12B   | 1408 x 1408          | Quantized version of `FLUX.1-Fill-dev`.                                                                                                                                           |
| `FLUX.1-Fill-dev`                     | Nov 21, 2024   | Rectified flow transformer                           | 12B   | 1408 x 1408            | Trained using guidance distillation (from `FLUX.1-Fill-pro`?), requires ~50 denoising steps                                                  |
| `FLUX.1-dev-Controlnet-Inpainting-Beta` | Oct 8, 2024    | Rectified flow transformer                         | 12B   | 1408 x 1408           | Finetuned for inpainting using a ControlNet approach providing the mask and the encoded masked image as conditioning signals, requires ~28 denoising steps                               |
| `FLUX.1-dev-Controlnet-Inpainting-Beta-Turbo` | Oct 8, 2024 | Latent diffusion model (Flux.1-dev), Rectified flow transformer              | 12B   | 1408 x 1408       | Distilled version of `FLUX.1-dev-Controlnet-Inpainting-Beta` using a LoRA model, optimized for 8 denoising steps process.                                                                            |
| `SDXL-1-0-inpainting`               | Sep 7, 2024    | U-Net based diffusion process                                     | 6.6B  | 1024x1024      | Two-stage latent diffusion process, inputs are extended with 4 additional channels for mask and encoded masked image, finetuned on inpainting samples           |
| `SD3-Controlnet-Inpainting`           | Jun 12, 2024   | Multimodal Diffusion Transformer                                            | 2B    | 1024x1024      | Finetuned ControlNet inpainting model based on SD3-medium.                                                                                                                     |
| `kandinsky-2-2-decoder-inpaint`       | Jul 6, 2023    | U-Net based diffusion process      | 2.2B  | 1024x1024      | Combines a transformer-based image prior model, a U-Net diffusion model, and a decoder; optimized for inpainting tasks.                                                        |
| `SD-2-inpainting`                     | Nov 23, 2022   | U-Net based diffusion process                                        | 865M  | 512x512        | Adaptation of SD2 base model with additional input channels for mask and encoded masked image, finetuned for inpainting tasks.                                                 |
| `DALL-E-2`                            | Apr 13, 2022   | U-Net based diffusion process (Glide)      | 6B    | 1024x1024      | Uses two upsampling models for enhanced resolution.                                                                         |


>📌 MidJourney isn't part of this benchmark as it isn't available under API


## Model evaluation

We evaluate model predictions based on the following criteria:
- Realism, how natural and lifelike does the inpainted region appear?
- Adaptability, does the inpainting align with the provided prompts or instructions?
- Unmask image preservation, Are the unmasked parts of the image left intact?
- Consistency, is the inpainted region consistent with the unmasked area in terms of lighting (shadows, brightness), reflections, style, perspective, textures, structure?
- Reproducibility, are the outputs stable in quality and alignment across the trials?
- Performance and costs, how long does it take to generate results, what are the GPU requirements?

> 👀 For each benchmark sample 3 model predictions are available in the following [figures](/images/results)


| Model                                              | Realism        | Adaptability   | Consistency    | Unmask preservation | Reproducibility | GPU memory <br> (GB) | Inference time <br> (s/image) | Cost <br> ($/1k edits) |
|----------------------------------------------------|----------------|----------------|----------------|----------------------|-----------------|-----------------------|---------------------|------------------------|
| *FLUX.1-Fill-dev*                                  | ⭐⭐⭐☆          | ⭐⭐⭐⭐          | ⭐⭐⭐☆          | ⭐⭐⭐⭐               | ⭐⭐⭐⭐           | 38                    | 26.5                | 8.8                      |
| *FLUX.1-Fill-dev-nf4*                              | ⭐⭐⭐☆          | ⭐⭐⭐⭐          | ⭐⭐⭐☆          | ⭐⭐⭐⭐               | ⭐⭐⭐⭐           | 20                    | 26.5                | 8.8                      |
| *FLUX.1-dev-Controlnet-Inpainting-Beta*           | ⭐⭐☆☆          | ⭐⭐☆☆          | ⭐⭐⭐☆          | ⭐⭐⭐⭐               | ⭐⭐⭐☆           | 39                     | 14.7                | 4,9                      |
| *FLUX.1-dev-Controlnet-Inpainting-Beta-Turbo*     | ⭐⭐☆☆          | ⭐⭐☆☆          | ⭐⭐☆☆          | ⭐⭐⭐⭐               | ⭐⭐⭐☆           | 40                    | 4.5                 | 1,5                      |
| *DALL-E 2*                                        | ⭐⭐☆☆          | ⭐☆☆☆          | ⭐⭐☆☆          | ⭐⭐⭐⭐               | ⭐⭐☆☆           | -                     | 14.5                | 20                     |
| *stable-diffusion-xl-1.0-inpainting-0.1*          | ⭐⭐☆☆          | ⭐☆☆☆          | ⭐⭐☆☆          | ⭐☆☆☆               | ⭐⭐☆☆           | 10                    | 2.1                 | 0.7                      |
| *stable-diffusion-2-inpainting*                   | ⭐☆☆☆          | ⭐☆☆☆          | ⭐☆☆☆          | ⭐☆☆☆               | ⭐⭐☆☆           | 4                     | 1.3                 | 0.4                      |
| *kandinsky-2-2-decoder-inpaint*                   | ⭐⭐☆☆          | ⭐☆☆☆          | ⭐☆☆☆          | ⭐☆☆☆               | ⭐☆☆☆           | 13                    | 9.3                 | 3.1                      |
| *SD3-Controlnet-Inpainting*                       | ☆☆☆☆          | ⭐⭐☆☆          | ⭐☆☆☆          | ☆☆☆☆               | ⭐⭐☆☆           | 26                    | 7.0                 | 2.3                      |


>*Inference time and cost were estimated on (1024, 1024) images using a NVIDIA A100 40GB card with an estimated rent cost of 1.2$/hour*

## Conclusion


### Further improvements

- A ControlNet approach could enable strong user guidance to add complex objects (position, shape, orientation, etc.). This might enable improvements similar to structured generation where LLM generation is forced to match specific rules instead of invited through prompting.
Another conditioning channel complementary to the semantic (prompt)


- Image embeddings to make accessorizing:
   - more straightforward, avoiding img -> text -> img
   - more aligned with user intents
   -
