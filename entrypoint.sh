#!/bin/sh


jupyter nbconvert --to notebook --execute test.ipynb --TemplateExporter.exclude_input=True \
 --ExecutePreprocessor.kernel_name='python3' --output test_notebook_executed