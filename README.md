# ☁️ CloudVault — Student File Storage System

A cloud-based student file storage application built using **AWS EC2, Amazon S3, IAM, CloudWatch, Flask, and Boto3**.

The application allows students to upload academic files through a web interface and securely store them in Amazon S3. The application also retrieves and displays the files stored in the S3 bucket.

---

## 📌 Project Overview

The main objective of this project is to build a simple cloud-based file storage system using AWS services.

Instead of storing files directly on a local computer, uploaded files are stored in **Amazon S3**, while the Flask web application runs on an **Amazon EC2** instance.

The EC2 instance uses an **IAM Role** to communicate with S3 without storing AWS access keys inside the application.

---

## 🎯 Objectives

- Deploy a web application on AWS EC2.
- Store uploaded files using Amazon S3.
- Use IAM roles for secure AWS service access.
- Monitor the EC2 instance using CloudWatch.
- Build a simple and user-friendly file storage interface.
- Understand how different AWS services work together.

---

## ✨ Features

- 📤 Upload files through a web interface.
- ☁️ Store files in Amazon S3.
- 📂 Display files stored in the S3 bucket.
- 🔐 Use IAM Role-based AWS authentication.
- 🖥️ Flask application hosted on EC2.
- 📊 EC2 monitoring through CloudWatch.
- 📱 Responsive and simple web interface.
- 📦 Maximum upload size of 10 MB.

---

## 🏗️ Architecture

```mermaid
flowchart TD

    A[Student / User<br/>Web Browser]

    B[AWS EC2<br/>Ubuntu + Flask Application]

    C[Boto3<br/>AWS SDK for Python]

    D[IAM Role<br/>Secure AWS Permissions]

    E[Amazon S3<br/>student-file-storage-project1]

    F[CloudWatch<br/>EC2 Monitoring]

    A -->|HTTP Port 80| B
    B --> C
    C --> D
    D --> E
    B --> F
