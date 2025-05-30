# **Credit Approval System**

A Django-based backend application to manage a credit approval system, including customer registration, loan eligibility checks, loan creation, and loan viewing functionalities. The application uses PostgreSQL for data storage and Docker for containerization.

---

## **Tech Stack**

- **Backend**: Django 4+, Django Rest Framework (DRF)
- **Database**: PostgreSQL
- **Task Queue**: Celery
- **Message Broker**: Redis
- **Containerization**: Docker, Docker Compose
- **Dependencies Management**: pip and `requirements.txt`

---

## **Setup and Installation**

### **Prerequisites**

- Docker and Docker Compose installed on your system.
- Clone this repository:
  ```bash
  git clone https://github.com/Raju1422/credit-approval-system.git
  cd credit-approval-system

  ```

## **Steps to Run the Application**

- Add **.env** file into the root directory

#### **Build and Run the Containers**

- Build and Run the Containers Use Docker Compose to build and start the containers:
    ```bash
    docker compose up -d --build
    ```

#### **Run Migrations**

- Inside the running container, apply migrations:

    ```bash
    docker exec -it credit_approval_system_django python manage.py makemigrations
    docker exec -it credit_approval_system_django python manage.py migrate

    ```

#### Ingest Initial Data (Using Celery)

- Trigger Celery tasks to ingest data from customer_data.xlsx and loan_data.xlsx.

    ```bash
    ## Enter Django shell inside the container
    docker exec -it credit_approval_system_django python manage.py shell
    ```

    ```bash
    # Inside the Django shell
    from core.tasks import ingest_customer_data, ingest_loan_data

    # Trigger the Celery tasks (file path should be relative to container)
    ingest_customer_data.delay('/app/customer_data.xlsx')
    ingest_loan_data.delay('/app/loan_data.xlsx')

    ```

#### **Access the Application**

- The application will be accessible at http://localhost:8000/.
