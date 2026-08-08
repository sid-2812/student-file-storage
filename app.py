from flask import Flask, render_template_string, request, redirect, url_for
import boto3
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# AWS S3 configuration
S3_BUCKET = "student-file-storage-project1"

# Create S3 client
s3 = boto3.client("s3")

# Maximum upload size: 10 MB
app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024


HTML = """
<!DOCTYPE html>
<html lang="en">

<head>

    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <title>CloudVault | Student File Storage</title>

    <style>

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: Arial, sans-serif;
            background: linear-gradient(135deg, #eef4ff, #f8faff);
            min-height: 100vh;
            color: #1f2937;
        }

        .navbar {
            background: #111827;
            color: white;
            padding: 18px 8%;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .logo {
            font-size: 22px;
            font-weight: bold;
        }

        .badge {
            background: #374151;
            padding: 7px 14px;
            border-radius: 20px;
            font-size: 13px;
        }

        .container {
            max-width: 950px;
            margin: 60px auto;
            padding: 20px;
        }

        .hero {
            text-align: center;
            margin-bottom: 35px;
        }

        .hero h1 {
            font-size: 42px;
            margin-bottom: 12px;
            color: #111827;
        }

        .hero p {
            color: #6b7280;
            font-size: 17px;
        }

        .card {
            background: white;
            border-radius: 18px;
            padding: 40px;
            box-shadow: 0 15px 40px rgba(0, 0, 0, 0.08);
            text-align: center;
        }

        .upload-icon {
            font-size: 50px;
            margin-bottom: 10px;
        }

        .card h2 {
            margin-bottom: 10px;
            color: #111827;
        }

        .card p {
            color: #6b7280;
            margin-bottom: 20px;
        }

        input[type="file"] {
            display: block;
            width: 100%;
            max-width: 450px;
            margin: 20px auto;
            padding: 14px;
            border: 2px dashed #cbd5e1;
            border-radius: 10px;
            background: #f8fafc;
            cursor: pointer;
        }

        .upload-btn {
            background: #2563eb;
            color: white;
            border: none;
            padding: 13px 30px;
            border-radius: 9px;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
        }

        .upload-btn:hover {
            background: #1d4ed8;
        }

        .message {
            margin-top: 20px;
            padding: 12px;
            border-radius: 8px;
            background: #ecfdf5;
            color: #047857;
        }

        .files-section {
            margin-top: 35px;
            text-align: left;
        }

        .files-section h2 {
            margin-bottom: 15px;
            color: #111827;
        }

        .file-list {
            list-style: none;
        }

        .file-item {
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: #f8fafc;
            border: 1px solid #e5e7eb;
            padding: 14px 18px;
            margin-bottom: 10px;
            border-radius: 10px;
        }

        .file-name {
            font-weight: 500;
        }

        .file-icon {
            margin-right: 8px;
        }

        .empty {
            color: #6b7280;
            padding: 15px;
            text-align: center;
        }

        .features {
            display: flex;
            justify-content: space-around;
            margin-top: 35px;
            gap: 20px;
            flex-wrap: wrap;
        }

        .feature {
            flex: 1;
            min-width: 180px;
            background: #f8fafc;
            padding: 20px;
            border-radius: 12px;
        }

        .feature h3 {
            font-size: 16px;
            margin-bottom: 7px;
        }

        .feature p {
            font-size: 13px;
            color: #6b7280;
            margin: 0;
        }

        footer {
            text-align: center;
            margin-top: 35px;
            color: #6b7280;
            font-size: 13px;
        }

        @media (max-width: 600px) {

            .hero h1 {
                font-size: 30px;
            }

            .card {
                padding: 25px;
            }

            .navbar {
                padding: 15px 5%;
            }

        }

    </style>

</head>


<body>


    <nav class="navbar">

        <div class="logo">
            ☁ CloudVault
        </div>

        <div class="badge">
            AWS S3 Storage
        </div>

    </nav>


    <main class="container">


        <section class="hero">

            <h1>
                Student File Storage
            </h1>

            <p>
                Securely upload and manage your academic files in the cloud.
            </p>

        </section>


        <section class="card">


            <div class="upload-icon">
                📁
            </div>


            <h2>
                Upload Your File
            </h2>


            <p>
                Select a document, image, or project file.
                Maximum size: 10 MB.
            </p>


            <form
                action="/upload"
                method="POST"
                enctype="multipart/form-data"
            >

                <input
                    type="file"
                    name="file"
                    required
                >

                <button
                    class="upload-btn"
                    type="submit"
                >
                    Upload to Cloud
                </button>

            </form>


            {% if message %}

                <div class="message">
                    {{ message }}
                </div>

            {% endif %}


            <div class="files-section">

                <h2>
                    📂 Stored Files
                </h2>


                {% if files %}

                    <ul class="file-list">

                        {% for file in files %}

                            <li class="file-item">

                                <span class="file-name">

                                    <span class="file-icon">
                                        📄
                                    </span>

                                    {{ file }}

                                </span>

                            </li>

                        {% endfor %}

                    </ul>

                {% else %}

                    <div class="empty">
                        No files uploaded yet.
                    </div>

                {% endif %}

            </div>


            <div class="features">


                <div class="feature">

                    <h3>
                        ☁ Cloud Storage
                    </h3>

                    <p>
                        Files are stored using Amazon S3.
                    </p>

                </div>


                <div class="feature">

                    <h3>
                        🔐 Secure Access
                    </h3>

                    <p>
                        AWS IAM controls application access.
                    </p>

                </div>


                <div class="feature">

                    <h3>
                        ⚡ Reliable
                    </h3>

                    <p>
                        Application hosted on AWS EC2.
                    </p>

                </div>


            </div>


        </section>


        <footer>

            AWS Cloud-Based Student File Storage System

        </footer>


    </main>


</body>

</html>
"""


@app.route("/")
def home():

    files = []

    try:

        response = s3.list_objects_v2(
            Bucket=S3_BUCKET
        )

        if "Contents" in response:

            files = [
                item["Key"]
                for item in response["Contents"]
            ]

    except Exception as error:

        print("S3 listing error:", error)


    return render_template_string(
        HTML,
        files=files
    )


@app.route("/upload", methods=["POST"])
def upload_file():

    if "file" not in request.files:

        return redirect(
            url_for("home")
        )


    file = request.files["file"]


    if file.filename == "":

        return redirect(
            url_for("home")
        )


    filename = secure_filename(
        file.filename
    )


    try:

        s3.upload_fileobj(
            file,
            S3_BUCKET,
            filename
        )

        message = (
            f"Successfully uploaded: {filename}"
        )


    except Exception as error:

        print(
            "Upload error:",
            error
        )

        message = (
            "Upload failed. "
            "Please check the AWS configuration."
        )


    files = []

    try:

        response = s3.list_objects_v2(
            Bucket=S3_BUCKET
        )

        if "Contents" in response:

            files = [
                item["Key"]
                for item in response["Contents"]
            ]

    except Exception as error:

        print(
            "S3 listing error:",
            error
        )


    return render_template_string(
        HTML,
        message=message,
        files=files
    )


if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=80,
        debug=False
    )
