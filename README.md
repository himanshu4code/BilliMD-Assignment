# Project Documentation

## Docker Setup

### Prerequisites
- Docker installed on your machine
- Docker Compose installed on your machine

### Running with Docker
1. Build and start the containers:
```bash
docker-compose up --build
```

2. The application will be available at:
- API: http://localhost:8000

## Authentication

### Available Roles
- `admin`
- `author`
- `user`

### Authentication Headers
To authenticate requests, include the following headers:

```http
x-user: <user>
x-role: <admin|user|author>
```

Example:
```http
x-user: 123456
x-role: admin
```

### Role-Based Access
1. Admin Role (`admin`)
   - Can read and delete all blogs

2. Admin Role (`author`)
   - Can read and update all blogs

3. User Role (`user`)
   - Can read all blogs

## API Endpoints

All endpoints require authentication headers mentioned above.

For detailed API documentation, please refer to the Swagger documentation at:
```
http://localhost:8000/docs
```
