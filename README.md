# Student Administration Website

This repository contains the code for a student administration system designed to manage and streamline various administrative tasks for the University of Connecticut.

## Features
- User Authentication
- Course Management
- Student Enrollment
- Data Management using DynamoDB
- RESTful API Endpoints

## Setup Instructions

1. **Clone the repository**:
   ```bash
   git clone https://github.com/zuhayrhuseni/Student-Administration-Website.git
   cd Student-Administration-Website
   
2. **Set up AWS credentials**:
   Ensure you have your AWS credentials configured to allow access to DynamoDB.
   
3. **Create DynamoDB tables**:
   Run the `createtable-*.py` scripts to create necessary tables in DynamoDB.
   ```bash
   python createtable-courses.py
   python createtable-subjects.py
   python createtable-users.py
   
4. **Populate initial data**:
   Use the `starterPopulation.py` script to populate the tables with initial data.
   ```bash
   python starterPopulation.py

## Usage

- **Running the backend**:
  Deploy the backend on AWS Lambda or your preferred server.
- **API Endpoints**:
  Use the provided scripts and API endpoints to interact with the system.
