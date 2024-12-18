# Stock Simulator Backend

## Project Overview

The **Stock Simulator Backend** provides an API service to simulate the growth or decrease of investments based on historical stock data. Users can input parameters like stock symbols, investment dates, and starting values, and the system calculates the percentage change, final value, and other key metrics.

This backend service complements the **Stock Investment Simulation Frontend** by supplying the necessary data and logic to power the investment simulations.

---

## **Key Features**

- **Stock Validation**: Validates stock symbols against a predefined exchange list.
- **Investment Simulation**: Calculates growth percentages and final values based on historical data.
- **REST API**: Features clear, RESTful endpoints for seamless frontend-backend communication.
- **Error Handling**: Advanced error logging and informative messages.
- **Modular Architecture**: Separation of concerns for scalable and maintainable code.

---

## **Backend Architecture**

The backend is built using **Flask**, following best practices for modularity and maintainability:

- **Separation of Concerns**: Organized by modules (app.py, config.py, routes.py, etc.).
- **Logging and Error Handling**: Includes structured logging and robust error handling.
- **Environment Configurations**: Manages settings through environment variables.
- **RESTful Endpoints**: For health checks, fetching exchanges, and simulating stock investments.

### **Project Structure**

```plaintext
stock-simulator-backend/
├── app.py                  # Main entry point
├── config/
│   ├── config.py           # Environment variable configurations
│   └── log_config.py       # Logging configurations
├── routes/
│   └── routes.py           # API routes
├── services/
│   ├── stock_simulator_service.py  # Stock simulation logic
│   └── exchange_service.py         # Exchange information logic
├── tests/                  # Unit tests with Pytest
├── postman/                # Postman collections and environments
├── requirements.txt        # Python dependencies
└── logs/
    └── app.log             # Application log files
```

---

## **Installation**

Follow these steps to set up the backend locally:

### **Prerequisites**

- Python 3.8+
- Pip (Python package manager)

### **Steps**

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/fnldesign/stock-simulator-backend.git
   cd stock-simulator-backend
   ```

2. **Set Up Virtual Environment**:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: `venv\Scripts\activate`
   ```

3. **Install Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables**:

   Create a `.env` file based on the provided `.env.sample` and set appropriate values.

5. **Run the Server**:

   ```bash
   python app.py
   ```

The backend will be accessible at `http://localhost:5000`. Test it with the `/api/health` endpoint.

---

## **Docker Setup**

To run the backend in a Docker container:

1. **Build the Docker Image**:

   ```bash
   docker build -t stock-simulator-backend .
   ```

2. **Run the Docker Container**:

   ```bash
   docker run -p 5000:5000 stock-simulator-backend
   ```

---

## **License**

This project is licensed under the **Creative Commons Attribution-NonCommercial 4.0 International License** (CC BY-NC 4.0).  
You are free to share and adapt the material under the following terms:

- **Attribution**: Credit the original authors, link to the license, and indicate any changes made.
- **NonCommercial**: You may not use the material for commercial purposes.

For details, see the [LICENSE.md](./LICENSE.md) file.

---

## **Contribution Instructions**

We are using **Git Flow** for branch management. To contribute:

1. **Fork the Repository**:

   ```bash
   git clone https://github.com/<your-username>/stock-simulator-backend.git
   cd stock-simulator-backend
   ```

2. **Create a Feature Branch**:

   ```bash
   git flow feature start <feature-name>
   ```

3. **Make Changes and Commit**:

   ```bash
   git add .
   git commit -m "Description of changes"
   ```

4. **Push the Branch**:

   ```bash
   git push origin feature/<feature-name>
   ```

5. **Open a Pull Request**: Submit your changes for review.

---

## **Contact**

For questions or suggestions, feel free to reach out:

- **Email**: fnldesign@hotmail.com
- **Open an Issue**: [GitHub Issues](https://github.com/fnldesign/stock-simulator-backend/issues)

---

Thank you for contributing to the Stock Investment Simulation Project! 🚀
