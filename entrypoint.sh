#!/bin/sh
# Test run for model inference notebook

jupyter nbconvert --to notebook --execute /04_model_inference.ipynb  --TemplateExporter.exclude_input=True \
 --ExecutePreprocessor.kernel_name='python3' --output 04_model_inference_executed  
