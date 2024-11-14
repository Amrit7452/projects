import tkinter as tk
from tkinter import ttk
from PIL import ImageGrab, Image
import cv2
import pytesseract

# Set the path to the Tesseract executable (adjust this path if needed)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

import numpy as np

# Hi-Lo card values
card_values = {
    '2': 1, '3': 1, '4': 1, '5': 1, '6': 1,
    '7': 0, '8': 0, '9': 0,
    '10': -1, 'J': -1, 'Q': -1, 'K': -1, 'A': -1
}

class CardCountingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Card Counting Blackjack")
        self.root.geometry("400x500")
        self.root.configure(bg="#2c3e50")  # Dark background for a modern look

        # Custom fonts and styles with larger sizes
        label_font = ("Helvetica", 16, "bold")
        button_font = ("Helvetica", 14)
        label_fg = "#ecf0f1"  # Light text color

        # Input for number of decks
        self.deck_label = tk.Label(root, text="Enter number of decks:", font=label_font, bg="#2c3e50", fg=label_fg)
        self.deck_label.pack(pady=10)
        self.deck_entry = tk.Entry(root, font=("Helvetica", 14))
        self.deck_entry.pack(pady=5)

        # Button to start the game
        self.start_button = tk.Button(root, text="Start", font=button_font, bg="#2980b9", fg="white", command=self.start_game)
        self.start_button.pack(pady=10)

        # Button to capture the screen and analyze the card
        self.capture_button = tk.Button(root, text="Capture Card", font=button_font, bg="#c0392b", fg="white", command=self.capture_and_detect)
        self.capture_button.pack(pady=10)

        # Labels to display the running count and true count
        self.running_count_label = tk.Label(root, text="Running Count: 0", font=label_font, bg="#2c3e50", fg=label_fg)
        self.running_count_label.pack(pady=10)
        self.true_count_label = tk.Label(root, text="True Count: 0", font=label_font, bg="#2c3e50", fg=label_fg)
        self.true_count_label.pack(pady=10)

        # Variables for card counting
        self.running_count = 0
        self.decks_left = 0

    def start_game(self):
        # Initialize the number of decks
        self.total_decks = int(self.deck_entry.get())
        self.decks_left = self.total_decks
        self.running_count = 0
        self.update_counts()

    def capture_screen(self):
        # Capture a region of the screen (modify the bbox to your card area)
        bbox = (100, 100, 400, 400)  # Example coordinates
        screenshot = ImageGrab.grab(bbox=bbox)
        screenshot.save("card_image.png")  # Save the captured image

    def detect_card_ocr(self):
        # Load the captured image
        image = Image.open('card_image.png')

        # Use Tesseract to detect text in the image
        card_text = pytesseract.image_to_string(image, config='--psm 6')

        # Clean up the text output
        card_text = card_text.strip().upper()

        # Check if the card is valid
        if card_text in card_values.keys():
            print(f"Card Detected: {card_text}")
            return card_text
        else:
            print("No valid card detected")
            return None

    def capture_and_detect(self):
        self.capture_screen()
        detected_card = self.detect_card_ocr()
        if detected_card:
            self.update_card_count(detected_card)

    def update_card_count(self, detected_card):
        if detected_card in card_values:
            self.running_count += card_values[detected_card]
            self.update_counts()

    def update_counts(self):
        # Update running count
        self.running_count_label.config(text=f"Running Count: {self.running_count}")

        # Calculate the true count (running count divided by remaining decks)
        true_count = self.running_count / self.decks_left if self.decks_left > 0 else 0
        self.true_count_label.config(text=f"True Count: {true_count:.2f}")

# Create the main application window
root = tk.Tk()
app = CardCountingApp(root)
root.mainloop()
