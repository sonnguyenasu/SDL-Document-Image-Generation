## How to use this repo:

### Step 1: Generate formula images: 

Running formula.py to generate 20k formula images

### Step 2: Generate document data:
*Optional* You can change config to generate data at configs/page.yaml. It is advised to change number of image to generate in the first run.

All text components are aranged in columns
```
python columns_layout.py --config_file configs/page.yaml
```
Text components are aranged freely
```
python flexible_layout.py --config_file configs/page.yaml
```

Options for args argument
```
  -h, --help            show this help message and exit
  -n NUM_CORE, --num_core NUM_CORE
                        # cores are used for generation
  -c CONFIG_FILE, --config_file CONFIG_FILE
```

Images would be saved at output/images.

## Visualization of the result:
 
```python data_manipulation/visualize.py```

The result will be saved at assets/illustration
