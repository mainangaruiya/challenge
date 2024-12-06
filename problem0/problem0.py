import argparse
import hashlib
from PIL import Image
import os
import random

def calculate_hash(file_path, algorithm="sha512"):
    """Calculate the hash of a file."""
    hash_func = hashlib.new(algorithm)
    with open(file_path, "rb") as f:
        while chunk := f.read(8192):
            hash_func.update(chunk)
    return hash_func.hexdigest()

def modify_image(input_image, output_image, prefix, algorithm="sha512"):
    """Modify an image file to match a hash prefix."""
    # Load the image
    image = Image.open(input_image)
    temp_output = output_image + ".tmp"
    
    # Add a small random change to image metadata
    metadata_key = "SpoofKey"
    counter = 0
    while True:
        # Embed metadata (or append non-visible bytes)
        metadata_value = f"SpoofValue{random.randint(0, 1e9)}"
        image.save(temp_output, format="PNG", pnginfo={metadata_key: metadata_value})
        
        # Calculate hash of the modified file
        file_hash = calculate_hash(temp_output, algorithm=algorithm)
        
        # Check if the hash matches the prefix
        if file_hash.startswith(prefix):
            os.rename(temp_output, output_image)
            print(f"Match found! Hash: {file_hash}")
            return True
        
        counter += 1
        if counter % 1000 == 0:
            print(f"Attempts: {counter}, Current hash: {file_hash[:len(prefix)]}")
