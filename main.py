import os
from app import app

# Ensure the data directory exists for XML storage
data_dir = os.path.join(os.path.dirname(__file__), 'data')
if not os.path.exists(data_dir):
    os.makedirs(data_dir)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
