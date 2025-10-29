"""
Simplified Mock CCTV Camera Server
This is a lightweight version that only requires Flask and Pillow
Perfect for quick testing with Power Automate
"""

from flask import Flask, Response, send_file
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import io
import time
import random

app = Flask(__name__)

class SimpleCCTVCamera:
    """Simple CCTV camera simulator"""
    
    def __init__(self):
        self.frame_count = 0
        
    def create_test_image(self):
        """Create a simple test image that simulates a CCTV feed"""
        # Create image
        width, height = 640, 480
        image = Image.new('RGB', (width, height), color='darkgray')
        draw = ImageDraw.Draw(image)
        
        # Add grid pattern
        for x in range(0, width, 50):
            draw.line([(x, 0), (x, height)], fill='gray', width=1)
        for y in range(0, height, 50):
            draw.line([(0, y), (width, y)], fill='gray', width=1)
        
        # Add random "motion" rectangles
        for _ in range(3):
            x = random.randint(0, width-100)
            y = random.randint(0, height-100)
            w = random.randint(30, 100)
            h = random.randint(30, 100)
            color = (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))
            draw.rectangle([x, y, x+w, y+h], fill=color, outline='white')
        
        # Add text overlay
        try:
            font = ImageFont.load_default()
        except:
            font = None
            
        # Add camera name
        draw.text((10, 10), "MOCK CCTV - CAMERA 01", fill='lime', font=font)
        
        # Add timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        draw.text((10, 30), timestamp, fill='lime', font=font)
        
        # Add frame counter
        self.frame_count += 1
        draw.text((10, 50), f"Frame: {self.frame_count}", fill='lime', font=font)
        
        # Add REC indicator
        draw.ellipse([width-50, 10, width-30, 30], fill='red')
        draw.text((width-80, 12), "REC", fill='white', font=font)
        
        # Convert to bytes
        img_buffer = io.BytesIO()
        image.save(img_buffer, format='JPEG')
        img_buffer.seek(0)
        
        return img_buffer

# Create camera instance
camera = SimpleCCTVCamera()

@app.route('/')
def home():
    """Home page with links to different endpoints"""
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Mock CCTV Camera</title>
        <style>
            body { 
                font-family: Arial, sans-serif; 
                max-width: 800px; 
                margin: 50px auto; 
                padding: 20px;
                background: #f0f0f0;
            }
            h1 { color: #333; }
            .endpoint { 
                background: white; 
                padding: 15px; 
                margin: 10px 0; 
                border-radius: 5px;
                box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            }
            a { 
                color: #007bff; 
                text-decoration: none; 
                font-weight: bold;
            }
            a:hover { text-decoration: underline; }
            img { 
                max-width: 100%; 
                margin-top: 20px; 
                border: 2px solid #333;
                border-radius: 5px;
            }
            code {
                background: #f4f4f4;
                padding: 2px 5px;
                border-radius: 3px;
            }
        </style>
    </head>
    <body>
        <h1>🎥 Mock CCTV Camera Server</h1>
        <p>This server simulates a CCTV camera for testing with Power Automate.</p>
        
        <h2>Available Endpoints:</h2>
        
        <div class="endpoint">
            <h3>📸 Get Snapshot</h3>
            <p>Returns a JPEG image from the camera</p>
            <p>URL: <a href="/snapshot" target="_blank">http://localhost:5000/snapshot</a></p>
            <p>Method: <code>GET</code></p>
            <p>Returns: <code>image/jpeg</code></p>
        </div>
        
        <div class="endpoint">
            <h3>📊 Get Camera Status</h3>
            <p>Returns JSON with camera information</p>
            <p>URL: <a href="/status" target="_blank">http://localhost:5000/status</a></p>
            <p>Method: <code>GET</code></p>
            <p>Returns: <code>application/json</code></p>
        </div>
        
        <h2>Current Snapshot:</h2>
        <img src="/snapshot" alt="Camera Snapshot" id="snapshot">
        
        <script>
            // Auto-refresh image every 5 seconds
            setInterval(function() {
                document.getElementById('snapshot').src = '/snapshot?' + new Date().getTime();
            }, 5000);
        </script>
        
        <h2>Power Automate Integration:</h2>
        <p>To use this in Power Automate:</p>
        <ol>
            <li>Use the HTTP action</li>
            <li>Set Method to GET</li>
            <li>Set URI to <code>http://localhost:5000/snapshot</code> or <code>http://YOUR_IP:5000/snapshot</code></li>
            <li>The response will contain the image data</li>
        </ol>
    </body>
    </html>
    """
    return html

@app.route('/snapshot')
def snapshot():
    """Return a snapshot image from the camera"""
    img_buffer = camera.create_test_image()
    return send_file(img_buffer, mimetype='image/jpeg')

@app.route('/status')
def status():
    """Return camera status as JSON"""
    return {
        "camera_id": "MOCK-CAM-01",
        "status": "online",
        "timestamp": datetime.now().isoformat(),
        "frame_count": camera.frame_count,
        "resolution": "640x480",
        "location": "Test Location",
        "type": "Mock CCTV Camera"
    }

if __name__ == '__main__':
    print("\n" + "="*50)
    print("Mock CCTV Camera Server")
    print("="*50)
    print("\nServer is running at: http://localhost:5000")
    print("\nEndpoints:")
    print("  Home Page:    http://localhost:5000/")
    print("  Snapshot:     http://localhost:5000/snapshot")
    print("  Status:       http://localhost:5000/status")
    print("\nPress Ctrl+C to stop the server")
    print("="*50 + "\n")
    
    app.run(host='0.0.0.0', port=5000, debug=True)