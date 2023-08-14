import os
import json
import zipfile
import base64
import tempfile
from subprocess import check_output, CalledProcessError
from flask import Flask, Response, request
from logging.config import dictConfig
import sys
sys.stdout.flush()

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})

JPLAG_FILE = "jplag-4.3.0-jar-with-dependencies.jar"
app = Flask(__name__)

def extract_result(zip_file_path):
    with zipfile.ZipFile(f"{zip_file_path}.zip", "r") as zip_ref:
        # Extract the JSON files from the zip file
        json_files = [file for file in zip_ref.namelist() if file.endswith(".json")]
        results = []

        # Process each JSON file
        for json_file in json_files:
            # Read the JSON content
            with zip_ref.open(json_file) as file:
                json_data = file.read()

            # Parse the JSON data
            data = json.loads(json_data)
            results.append(data)

        return results

@app.route('/', methods=['POST'])
def detect_plagiarism():
    extension = request.json.get('extension')
    submissions = request.json.get('submissions', [])
    response = {"errors": []}

    # Create a temporary directory to store the submission
    # temp_dir = tempfile.mkdtemp()
    with tempfile.TemporaryDirectory() as temp_dir:
        for submission in submissions:
            # Save the submission to a temporary file
            # submission_path: str = f"{temp_dir}/{submission['id']}.{extension}"
            submission_path = os.path.join(temp_dir, f"{submission['id']}.{extension}")
            with open(submission_path, 'wb') as file:
                # Decode the submission from base64
                file.write(base64.b64decode(submission['code']))

        results_file = os.path.join(temp_dir, "results")
        command = ["java", "-jar", JPLAG_FILE, temp_dir, "-l", extension, "-r", results_file]
        # java -jar jplag-4.3.0-jar-with-dependencies.jar /tmp/teste/ -l cpp -r /tmp/teste/r1/results
        try:
            output_response = check_output(command).decode('utf-8')
            response["command_output"] = output_response
        except CalledProcessError as error:
            response["errors"].append(str(error.output))
        except Exception as error:
            response["errors"].append(str(error))
        else:
            response["results"] = extract_result(results_file)

        return Response(
            json.dumps(response),
            status=200,
            mimetype='application/json',
        )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
