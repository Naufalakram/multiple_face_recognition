from flask import Flask, render_template , request
import subprocess
import threading
import json

dataset = "dataset.json"

app = Flask(__name__, static_folder='assets', template_folder='templates')

# Variable to track the status of the main.py process
main_process = None

# Initialize the scan status as False
scan_status = False

def run_main_py():
    global main_process, scan_status
    scan_status = True
    main_process = subprocess.Popen(['python', 'main.py'], cwd='.')
    main_process.wait()  # Wait for the process to complete
    main_process = None  # Reset the process variable
    print("main.py process completed.")
    scan_status = False


def run_main2_py():
    global main_process, scan_status
    scan_status = True
    main_process = subprocess.Popen(['python', 'main2.py'], cwd='.')
    main_process.wait()  # Wait for the process to complete
    main_process = None  # Reset the process variable
    print("main2.py process completed.")
    scan_status = False

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/scan_face')
def scan_face():
    global main_process

    if main_process is None or main_process.poll() is not None:
        # If the main.py process is not running or has completed
        # Start a new thread to run the main.py process
        thread = threading.Thread(target=run_main_py)
        thread.start()
        return  render_template('scan_face.html')

    return "Scanning face is already in progress."

# Create a route that checks for scan_status
@app.route('/scan_status')
def check_scan_status():
    global scan_status
    return {'scan_status': scan_status}

@app.route('/tambah_karyawan')
def tambah_karyawan():
    # open the dataset file
    with open(dataset, 'r') as f:
        data = json.load(f)
        len_data = len(data)

    print(data)

    return render_template('tambah_karyawan.html', data=data, length=len_data)

@app.route('/tambah_karyawan', methods=['POST'])
def tambah_karyawan_post():
    nama = request.form['nama']
    nik = request.form['nik']
    # print(nama)
    # print(nik)

    # open the dataset file
    with open(dataset, 'r') as f:
        data = json.load(f)

    # insert the new data
    data.append({
        'name': nama,
        'nik': nik
    })

    # save the dataset file
    with open(dataset, 'w') as f:
        json.dump(data, f)

    # return the json
    return {'status': 'OK'}

# dibawah ni untuk buka main2.py dan loading page
@app.route('/scan_face2')
def scan_face2():
    global main_process

    if main_process is None or main_process.poll() is not None:
        # If the main.py process is not running or has completed
        # Start a new thread to run the main.py process
        thread = threading.Thread(target=run_main2_py)
        thread.start()
        return  render_template('scan_face.html')

    return "Scanning face is already in progress."


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
