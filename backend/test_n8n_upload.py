import requests

url = "http://127.0.0.1:8000/upload_multiple_files"

# Create dummy files
files = [
    ('files', ('test1.txt', b'This is test file 1', 'text/plain')),
    ('files', ('test2.txt', b'This is test file 2', 'text/plain'))
]

print(f"Sending files to {url}...")
try:
    response = requests.post(url, files=files)
    
    if response.status_code == 200:
        print("Success!")
        print("Response:", response.json())
    else:
        print(f"Failed with status {response.status_code}")
        print(response.text)
except Exception as e:
    print(f"Error: {e}")
    print("Make sure the server is running (uvicorn main:app --reload)")
