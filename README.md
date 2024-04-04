# BizCardX: Extracting Business Card Data with OCR


## Problem Statement:
### You have been tasked with developing a Streamlit application that allows users to upload an image of a business card and extract relevant information from it using easyOCR. The extracted information should include:

### Company name
### Cardholder name
### Designation
### Mobile number
### Email address
### Website URL
### Area
### City
### State
### Pin code
### The extracted information should then be displayed in the application’s graphical user interface (GUI). Additionally, the application should allow users to save the extracted information into a database along with the uploaded business card image. The database should be able to store multiple entries, each with its own business card image and extracted information.

# Approach
## Install the required packages:
### You will need to install Python, Streamlit, easyOCR, and a database management system like SQLite or MySQL.
# Design the user interface:
### Create a simple and intuitive user interface using Streamlit that guides users through the process of uploading the business card image and extracting its information. Use widgets like file uploaders, buttons, and text boxes to make the interface more interactive.
# Implement image processing and OCR:
### Use easyOCR to extract the relevant information from the uploaded business card image.
### Apply image processing techniques like resizing, cropping, and thresholding to enhance the image quality before passing it to the OCR engine.
# Display the extracted information:
### Once the information has been extracted, display it in a clean and organized manner in the Streamlit GUI.
### Use widgets like tables, text boxes, and labels to present the information.
# Implement database integration:
### Use a database management system (e.g., SQLite or MySQL) to store the extracted information along with the uploaded business card image.
### Utilize SQL queries to create tables, insert data, retrieve data, update records, and allow users to delete entries through the Streamlit UI.
# Project Requirements
### Skills in image processing, OCR, GUI development, and database management.
### Careful design and planning of the application architecture for scalability, maintainability, and extensibility.
### Good documentation and code organization.
