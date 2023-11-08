from flask import Flask, request, send_file, render_template
import io
import csv
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process_file():
    uploaded_file = request.files['file']

    if uploaded_file:
        # Save the uploaded file to a temporary location
        temp_file_path = f"temp_{uploaded_file.filename}"
        uploaded_file.save(temp_file_path)

        # Process the uploaded CSV file
        extracted_data = process_csv(temp_file_path)

        # Create a file-like object for sending the processed data
        output = io.BytesIO()
        output.write(extracted_data.encode('utf-8'))
        output.seek(0)

        return send_file(output, as_attachment=True, download_name="processed_data.txt")

    return "No file uploaded.", 400

def process_csv(csv_file_path):
    # Initialize an empty list to store the extracted data
    extracted_data = []

    # Open and read the CSV file
    with open(csv_file_path, 'r', encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)  # Skip the header row

        for row in csv_reader:
            if len(row) >= 7:
                list_type = row[0]
                name = row[1]
                prospect_ut_eid = row[5]
                address = row[15]
                city = row[16]
                state = row[17]
                country = row[18]
                zipc = row[19]
                email = row[14]
                # birth_date = row[9]

                # if birth_date != 'Birth Date':
                #     d_obj = datetime.strptime(birth_date, '%d-%b-%Y')
                #     formatted_d = d_obj.strftime('%m %d %Y')
                # else:
                #     formatted_d = 'N/A'

                officer = row[3]

                # Append the extracted data in the desired format
                extracted_data.append(
                    f"{officer}\n{list_type}\n{prospect_ut_eid}\n\n{name}\n{address}\n{city} {state} {country} {zipc}\n{email}\n")
                    # {formatted_d}

    # Join the extracted data with line breaks
    result = '\n'.join(extracted_data)

    return result

if __name__ == '__main__':
    app.run(debug=True)
