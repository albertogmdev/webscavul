# WEBSCAVUL

**Webscavul** is a versatile and user-friendly web security vulnerability scanner that helps you identify, report, and manage common vulnerabilities in web applications. Built with Python and Next.js.

![alt text](https://github.com/albertogmdev/webscavul/blob/master/homepage-screenshot.jpg "Webscavul Homepage")

## Features

- **Automated Vulnerability Scanning**: Detects common vulnerabilities and misconfigurations in your webpage.
- **Custom Scan Profiles**: Configure full or header scan.
- **Interactive Dashboard**: Visualize scan results and vulnerability details in real time.
- **Modular Architecture**: Easily extend scanning capabilities with custom modules.
- **Report Generation**: Webscavul generates a resume report and a Kanban board for managing tasks.
- **Language Model Generation**: Integrates Groq cloud in order to generate custom solutions.
- **Docker Support**: Deploy and run Webscavul quickly using Docker.

## Tech Stack

- **Backend**: Python with FastAPI
- **Frontend**: Next.js, SCSS, HTML
- **Containerization**: Docker

## Installation

> **Note:** It is recommended to use Docker to deploy Webscavul. If you do not have Docker installed, please [download and install Docker here](https://docs.docker.com/get-docker/).

### 1. Clone the Repository

```bash
git clone https://github.com/albertogmdev/webscavul.git
cd webscavul
```

### 2. Create Your `.env` File

Copy the example environment file and update it with your own configuration if necessary:

```bash
cp .env.example .env
```

> The `.env` file is used to configure the database connection, application ports, and API URLs.  
> Example contents:
> ```
> DB_NAME=webscavul
> DB_HOST=mariadb
> DB_PORT=3306
> DB_USER=albertogmdev
> DB_ROOT_USER=root
> DB_PASSWORD=password
> APP_PORT=3000
> API_PORT=8000
> API_URL="localhost:${API_PORT}"
> GROQ_API_KEY="YOUR API KEY HERE"
> NEXT_PUBLIC_API_URL="localhost:${API_PORT}"
> ```
> You can change these values to match your environment or requirements.

#### ⚡️ Language Model Generation (Groq Cloud API Key)

If you want to use the model generation functionality, you need to obtain a GROQ_API_KEY from Groq Cloud.

- Sign up or log in at [Groq Platform](https://console.groq.com/).
- Go to your dashboard and generate an API key.
- Copy your key and set it in your `.env` file:
  ```
  GROQ_API_KEY="your_actual_groq_api_key"
  ```
- Without this key, model generation features will not be available.

### 3. Run with Docker

```bash
docker compose up --build
```

## Usage

1. Open your browser and navigate to `http://localhost:3000` (or the port you configured in .env file).
2. Input target URL and scan type.
3. Start a scan.
4. View results in the detail report view or manage found vulnerabilities through Kanban board.

## Contributing

Contributions are welcome!

## Authors

- [Alberto González Martínez](https://github.com/albertogmdev)

## Acknowledgements

- Inspired by OWASP ZAP, Nikto, and other open-source scanning tools.
- Thanks to the open-source community for libraries and test cases.

## Security

If you find a security issue, please report it directly to the repository owner or open a private issue.

---