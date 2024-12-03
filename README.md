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

Models will be scored based on 6 evaluation criteria:
- Realism, how natural and lifelike does the inpainted region appear?
- Adaptability, does the inpainting align with the provided prompts or instructions?
- Unmask image preservation, Are the unmasked parts of the image left intact?
- Consistency, is the inpainted region consistent with the unmasked area in terms of lighting (shadows, brightness), reflections, style, perspective, textures, structure?
- Reproducibility, are the outputs stable in quality and alignment across the trials?
- Performance and costs, how long does it take to generate results, what are the GPU requirements?

TODO resolution?
