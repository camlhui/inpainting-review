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

Traditional methods pioneered the concept of inpainting, really took of with deep learning. It enabled to fill large regions with complex structures, maintaining global semantic consistency and this in an automated fashion with great generalization capabilities.

Among the deep learning methods, all the state of the art approaches belongs to the latent diffusion models family. They are the only one supporting text guidance, arbitrary masks and mega-pixel resolution.

TODO

Model
- publication date
- author
- architecture
-

## Model evaluation

> 👀 For each benchmark sample 3 model predictions are available in the following [figures](/images/results)

We evaluate model predictions based on the following criteria:
- Realism, how natural and lifelike does the inpainted region appear?
- Adaptability, does the inpainting align with the provided prompts or instructions?
- Unmask image preservation, Are the unmasked parts of the image left intact?
- Consistency, is the inpainted region consistent with the unmasked area in terms of lighting (shadows, brightness), reflections, style, perspective, textures, structure?
- Reproducibility, are the outputs stable in quality and alignment across the trials?
- Performance and costs, how long does it take to generate results, what are the GPU requirements?


| Model                                              | Realism        | Adaptability   | Consistency    | Unmask preservation | Reproducibility | GPU memory <br> (GB) | Inference time <br> (s/image) | Cost <br> ($/1k edits) |
|----------------------------------------------------|----------------|----------------|----------------|----------------------|-----------------|-----------------------|---------------------|------------------------|
| *FLUX.1-Fill-dev*                                  | ⭐⭐⭐☆          | ⭐⭐⭐⭐          | ⭐⭐⭐☆          | ⭐⭐⭐⭐               | ⭐⭐⭐⭐           | 38                    | 26.5                | 8.8                      |
| *FLUX.1-Fill-dev-nf4*                              | ⭐⭐⭐☆          | ⭐⭐⭐⭐          | ⭐⭐⭐☆          | ⭐⭐⭐⭐               | ⭐⭐⭐⭐           | 20                    | 26.5                | 8.8                      |
| *FLUX.1-dev-Controlnet-Inpainting-Beta*           | ⭐⭐☆☆          | ⭐⭐☆☆          | ⭐⭐⭐☆          | ⭐⭐⭐⭐               | ⭐⭐⭐☆           | 39                     | 14.7                | 4,9                      |
| *FLUX.1-dev-Controlnet-Inpainting-Beta-Turbo*     | ⭐⭐☆☆          | ⭐⭐☆☆          | ⭐⭐☆☆          | ⭐⭐⭐⭐               | ⭐⭐⭐☆           | 40                    | 4.5                 | 1,5                      |
| *dall-e-2*                                        | ⭐⭐☆☆          | ⭐☆☆☆          | ⭐⭐☆☆          | ⭐⭐⭐⭐               | ⭐⭐☆☆           | -                     | 14.5                | 20                     |
| *stable-diffusion-xl-1.0-inpainting-0.1*          | ⭐⭐☆☆          | ⭐☆☆☆          | ⭐⭐☆☆          | ⭐☆☆☆               | ⭐⭐☆☆           | 10                    | 2.1                 | 0.7                      |
| *stable-diffusion-2-inpainting*                   | ⭐☆☆☆          | ⭐☆☆☆          | ⭐☆☆☆          | ⭐☆☆☆               | ⭐⭐☆☆           | 4                     | 1.3                 | 0.4                      |
| *kandinsky-2-2-decoder-inpaint*                   | ⭐⭐☆☆          | ⭐☆☆☆          | ⭐☆☆☆          | ⭐☆☆☆               | ⭐☆☆☆           | 13                    | 9.3                 | 3.1                      |
| *controlnet-canny-sdxl-1.0*                       | ☆☆☆☆          | ⭐☆☆☆          | ☆☆☆☆          | ⭐⭐⭐☆               | ⭐⭐⭐☆           | 17                    | 3.3                 | 1.1                      |
| *SD3-Controlnet-Inpainting*                       | ☆☆☆☆          | ⭐⭐☆☆          | ⭐☆☆☆          | ☆☆☆☆               | ⭐⭐☆☆           | 26                    | 7.0                 | 2.3                      |


>*Inference time and cost were estimated on (1024, 1024) images using a NVIDIA A100 40GB card with an estimated rent cost of 1.2$/hour*

## Conclusion
