from flask import Flask, render_template, request, send_file
import csv
import os
import tempfile

app = Flask(__name__)

# Function to process a single CSV file
def process_csv(file_path, writer):
    with open(file_path, 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) >= 33 and row[33].strip().lower() == "united states":
                linkedin_url = row[48] if len(row) >= 49 else ""
                first_name = row[0]
                last_name = row[1]
                gender = row[2]
                current_job_title = row[6]
                city = row[30]
                state = row[32]
                country = row[33]
                phone_numbers = row[5]
                email_addresses = row[4]
                company_size = row[12]
                industry = row[14]
                writer.writerow([linkedin_url, first_name, last_name, gender, current_job_title, city, state, country, phone_numbers, email_addresses, company_size, industry])

# Function to process all CSV files in a folder
def process_folder(folder_path):
    with tempfile.NamedTemporaryFile(mode='w', delete=False, newline='', encoding='utf-8') as temp_file:
        writer = csv.writer(temp_file)
        writer.writerow(["LinkedinProfileURL", "FirstName", "LastName", "Gender", "Curent Job Title", "City", "State", "Country", "PhoneNumbers", "Emailaddresses", "CompanySize", "Industry"])
        for filename in os.listdir(folder_path):
            if filename.endswith('.csv'):
                file_path = os.path.join(folder_path, filename)
                process_csv(file_path, writer)
        return temp_file.name

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_csv', methods=['POST'])
def generate_csv():
    folder_path = request.form['folderPath']
    output_file = process_folder(folder_path)
    return send_file(output_file, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
