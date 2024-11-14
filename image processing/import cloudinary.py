import cloudinary
import cloudinary.uploader
import tkinter as tk
from tkinter import filedialog, scrolledtext
import requests
import webcolors  

# Configure Cloudinary
cloudinary.config(
    cloud_name="do5jb8irj",
    api_key="571294314387526",
    api_secret="DSmyvjXsRiHB4IYljKOOorV1fFU",  
    secure=True
)

# Google Gemini API URL and key
api_url = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateText'
api_key = 'AIzaSyD6DpwEvN94Vf_um1yITIk5wU_nD8CnrDU'  # Replace with your Gemini API key

def get_closest_color_name(hex_code):
    try:
        # Direct match
        return webcolors.hex_to_name(hex_code)
    except ValueError:
        # Closest match if there's no direct CSS3 name
        rgb = webcolors.hex_to_rgb(hex_code)
        min_distance = None
        closest_color = None
        for name, color_rgb in webcolors.CSS3_NAMES_TO_HEX.items():
            distance = sum((component - ref_component) ** 2 for component, ref_component in zip(rgb, webcolors.hex_to_rgb(color_rgb)))
            if min_distance is None or distance < min_distance:
                min_distance = distance
                closest_color = name
        return closest_color

def generate_response(color_names):
    # Send a prompt to Google Gemini API
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }

    prompt_text = f"Suggest color combinations for clothing with the following colors: {', '.join(color_names)}."

    data = {
        "prompt": {
            "text": prompt_text
        }
    }

    response = requests.post(api_url, headers=headers, json=data)
    
    if response.status_code == 200:
        response_json = response.json()
        try:
            return response_json['candidates'][0]['output']['text'].strip()
        except KeyError as e:
            return f"Unexpected response structure: {e}"
    else:
        return f"Error: {response.status_code} - {response.text}"

def upload_and_analyze_images(image_paths):
    color_names = []
    
    for image_path in image_paths:
        # Upload image to Cloudinary and extract dominant colors
        upload_result = cloudinary.uploader.upload(image_path, colors=True)
        
        # Extract the most dominant color hex code
        if "colors" in upload_result and upload_result["colors"]:
            hex_color = upload_result["colors"][0][0]  # First color hex (most dominant)
            color_name = get_closest_color_name(hex_color)  # Convert hex to color name
            color_names.append(color_name)
        else:
            color_names.append("Unknown")
    
    return color_names

def display_color_combinations():
    # Open file dialog to select images
    image_paths = filedialog.askopenfilenames(filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])
    
    # Limit to 5 images
    if len(image_paths) > 5:
        text_area.config(state=tk.NORMAL)
        text_area.delete(1.0, tk.END)
        text_area.insert(tk.END, "Please select up to 5 images only.")
        text_area.config(state=tk.DISABLED)
        return

    # Upload and analyze images for color combinations
    color_names = upload_and_analyze_images(image_paths)
    
    # Generate response from Google Gemini
    suggestions = generate_response(color_names)
    
    # Display results in the text area
    text_area.config(state=tk.NORMAL)
    text_area.delete(1.0, tk.END)
    text_area.insert(tk.END, "Suggested Color Combinations:\n\n")
    text_area.insert(tk.END, suggestions)
    text_area.config(state=tk.DISABLED)

# Setting up the GUI window
window = tk.Tk()
window.title("Clothing Color Combination Suggestion")

# Label
label = tk.Label(window, text="Upload images of clothes for color combination suggestions:")
label.pack(pady=10)

# Button to upload images and get color combinations
button = tk.Button(window, text="Get Color Combinations", command=display_color_combinations)
button.pack(pady=10)

# ScrolledText widget to display the output
text_area = scrolledtext.ScrolledText(window, wrap=tk.WORD, width=70, height=15, state=tk.DISABLED)
text_area.pack(padx=10, pady=10)

# Running the GUI loop
window.mainloop()
