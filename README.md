# Flask API with Swagger, MongoDB Atlas, and Google Cloud Run

This project is a Python-based **Flask API** application that provides multiple endpoints for various functionalities. The project integrates with **MongoDB Atlas** for database operations and serves API documentation using **Swagger (Flasgger)**. It is deployed on **Google Cloud Platform (GCP)** using **Google Cloud Run** for scalability and reliability.

---


## **Features**

- **Multiple API Endpoints**:
  - A variety of endpoints to serve data and perform actions.
  - Easy integration with front-end applications or third-party systems.
  
- **API Documentation**:
  - Fully interactive API documentation generated using Swagger UI, available at `/apidocs/`.

- **Database**:
  - Secure and scalable integration with **MongoDB Atlas**.

- **Cloud Deployment**:
  - Hosted on **Google Cloud Run**, providing seamless scaling and HTTPS by default.

- **Modern Tech Stack**:
  - Built with **Python 3.9** and **Flask** for simplicity and efficiency.

---

## **Endpoints Overview**

### **API Endpoints**

| Endpoint            | Method | Description                         | Sample Response                                                                                          |
|---------------------|--------|-------------------------------------|--------------------------------------------------------------------------------------------------|
| `/`                 | `GET`  | Example endpoint returning JSON.    | `{ "message": "This is an example response." }`                                                        |

### **Swagger Documentation**

- **URL**: `https://codingsphere-811368486283.us-central1.run.app/apis/`
- **Description**: Interactive Swagger UI for exploring the API.
- **JSON Specification**: Available at `/v1/spec`.

---

## **Tech Stack**

| Component          | Technology                              |
|---------------------|-----------------------------------------|
| **Language**        | Python 3.9                             |
| **Framework**       | Flask                                  |
| **Database**        | MongoDB Atlas                          |
| **API Documentation** | Swagger (via Flasgger)               |
| **Cloud Deployment**| Google Cloud Run                       |

---

## **Project Structure**


```plaintext
project/
├── src/
│   ├── app.py            # Main Flask application entry point
│   ├── controllers/      # Directory containing API route definitions
│   ├── models/           # Directory containing MongoDB schema models
│   ├── config/           # Directory for configuration files (e.g., environment, constants)
│   └── helpers/          # Directory for utility and helper functions
├── swagger.yml           # API documentation (Swagger specification in YAML format)
├── main.py               # Application entry point to start the Flask server
├── requirements.txt      # File containing Python dependencies for the project
├── Dockerfile            # Configuration file for containerizing the application
├── cloudbuild.yaml       # Configuration file for Google Cloud Build deployment
└── templates/            # Directory for HTML files used by the application (if applicable)
```
---

## **Setup and Installation**

### **Prerequisites**

1. **Python 3.9** installed on your local machine.
2. A **MongoDB Atlas** cluster with a connection string.
3. **Google Cloud CLI** installed and authenticated.

---

### **Local Development**

Follow these steps to set up and run the project locally:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-repo/project.git
   cd project


## run in local env
```shell
python3.9 main.py
```


## Dependency
Pre-requisite:Python 3.9

Windows/mac/linux
gcloud cli

## CLI Deployment

```bash
gcloud auth activate-service-account --key-file={key_file}
gcloud config set project {PROJECT_ID}
gcloud builds submit --config cloudbuild.yaml
```

