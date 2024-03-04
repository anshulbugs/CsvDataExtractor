from flask import Flask, render_template, request, jsonify,send_file
import csv
import os

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
def process_folder(folder_path, output_file):
    with open(output_file, 'w', newline='', encoding='utf-8') as output:
        writer = csv.writer(output)
        writer.writerow(["LinkedinProfileURL", "FirstName", "LastName", "Gender", "Curent Job Title", "City", "State", "Country", "PhoneNumbers", "Emailaddresses", "CompanySize", "Industry"])
        for filename in os.listdir(folder_path):
            if filename.endswith('.csv'):
                file_path = os.path.join(folder_path, filename)
                process_csv(file_path, writer)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_csv', methods=['POST'])
def generate_csv():
    folder_path = request.form['folderPath']
    output_file = os.path.join(os.path.dirname(__file__), request.form['fileName'] + '.csv')
    process_folder(folder_path, output_file)
    file_path = os.path.abspath(output_file)  # Get the absolute path of the generated file
    return send_file(output_file, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
