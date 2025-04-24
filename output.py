import csv
import requests
from PIL import Image
from transformers import AutoProcessor, AutoModelForCausalLM
import torch

# Setup device and model configuration
device = "cuda:0" if torch.cuda.is_available() else "cpu"
torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

model = AutoModelForCausalLM.from_pretrained("microsoft/Florence-2-base", torch_dtype=torch_dtype, trust_remote_code=True).to(device)
processor = AutoProcessor.from_pretrained("microsoft/Florence-2-base", trust_remote_code=True)

# Function to run the model for a given task prompt and image
def run_example(task_prompt, image_url):
    image = Image.open(requests.get(image_url, stream=True).raw)
    inputs = processor(text=task_prompt, images=image, return_tensors="pt").to(device, torch_dtype)
    
    generated_ids = model.generate(
        input_ids=inputs["input_ids"],
        pixel_values=inputs["pixel_values"],
        max_new_tokens=6,
        num_beams=1
    )
    generated_text = processor.batch_decode(generated_ids, skip_special_tokens=False)[0]

    # Process the generation result (you can customize this as per your needs)
    parsed_answer = processor.post_process_generation(generated_text, task=task_prompt, image_size=(image.width, image.height))
    
    return parsed_answer

# Read sample_test.csv and write to output.csv
input_csv = 'sample_test.csv'
output_csv = 'output.csv'

possible_entity_names = ["item_volume", "wattage", "voltage", "maximum_weight_recommendation", "item_weight", "height", "depth", "width"]

with open(input_csv, mode='r') as infile, open(output_csv, mode='w', newline='') as outfile:
    reader = csv.DictReader(infile)
    fieldnames = reader.fieldnames + ['predicted_value']  # Add new field for predictions
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)

    writer.writeheader()

    for row in reader:
        entity_name = row['entity_name']
        image_url = row['image_link']

        if entity_name in possible_entity_names:
            task_prompt = f"What is the {entity_name} of the item?"
            predicted_value = run_example(task_prompt, image_url)
            row['predicted_value'] = predicted_value
        else:
            row['predicted_value'] = ''

        writer.writerow(row)
