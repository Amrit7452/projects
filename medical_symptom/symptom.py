import tkinter as tk
import matplotlib.pyplot as plt
import google.generativeai as genai 

genai.configure(api_key="AIzaSyCYZZ9rA01Z1XO54VYCL_mjmJZ_0R8Ech0")




def search_disease():
    disease_name = disease_entry.get()
    response = genai.generate_text(prompt=f"What are the symptoms of {disease_name}?")
    symptoms = response.text
    display_symptoms(symptoms)
    generate_case_data(disease_name)







def search_disease():
    disease_name = disease_entry.get()
    response = genai.generate_text(prompt=f"What are the symptoms of {disease_name}?")
    symptoms = response.text
    display_symptoms(symptoms)
    generate_case_data(disease_name)




def display_symptoms(symptoms):
    symptoms_text = tk.Text(window)
    symptoms_text.insert(tk.END, symptoms)
    symptoms_text.grid(row=2, column=0, columnspan=2)

def generate_case_data(disease_name):
    
    cases = [100, 150, 200, 180, 220]
    days = [1, 2, 3, 4, 5]

    # Create a plot
    plt.plot(days, cases)
    plt.title(f"Cases of {disease_name}")
    plt.xlabel("Days")
    plt.ylabel("Cases")
    plt.show()


window = tk.Tk()
window.title("Disease Information App")

disease_label = tk.Label(window, text="Enter Disease Name:")
disease_entry = tk.Entry(window)
search_button = tk.Button(window, text="Search", command=search_disease)

disease_label.grid(row=0, column=0)
disease_entry.grid(row=0, column=1)
search_button.grid(row=1, column=1)


window.mainloop()