#!/bin/sh
# If mode is 1, run training + inference mode, otherwise just run the inference

if [ $MODE==1 ]
then 
 echo "Training mode"
 # Data collection
 python 01_data_collection.py
 
 # Feature Engineering
 jupyter nbconvert --to notebook --execute 02_feature_engineering.ipynb --TemplateExporter.exclude_input=True \
 --ExecutePreprocessor.kernel_name='python3' --output 02_notebook_executed
 
 # Model Training
 jupyter nbconvert --to notebook --execute 03_model_training.ipynb --TemplateExporter.exclude_input=True \
 --ExecutePreprocessor.kernel_name='python3' --output 03_notebook_executed
 
 # Model Inference
  jupyter nbconvert --to notebook --execute /04_model_inference.ipynb  --TemplateExporter.exclude_input=True \
 --ExecutePreprocessor.kernel_name='python3' --output 04_model_inference_executed  

else
  echo "Inference mode"
  # Since the mode wasn't specified just run the model inference on new pull request
  jupyter nbconvert --to notebook --execute /04_model_inference.ipynb  --TemplateExporter.exclude_input=True \
 --ExecutePreprocessor.kernel_name='python3' --output 04_model_inference_executed
fi
