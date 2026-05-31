# Venturo API

Venturo is a community-driven platform for discovering, organizing, and joining outdoor experiences. Users can create events, participate in activities, offer rides, leave reviews, comment on experiences, and connect with like-minded people.

## Features

### Experiences
- Create, update, and delete outdoor experiences
- Browse upcoming and past experiences
- Search experiences by keyword
- Filter by category, location, difficulty, and spontaneity
- Sort by date, price, popularity, and ratings

### Participation
- Join experiences
- Track participant counts
- Monitor available spots

### Reviews
- Leave ratings and reviews for completed experiences
- Calculate average ratings
- View review history

### Comments
- Comment on experiences
- Comment on ride offers
- Update and delete your own comments

### Ride Sharing
- Offer rides to experiences
- Browse available ride offers
- Associate rides with experiences or create standalone rides

### Favorites
- Save experiences to favorites
- View favorite experiences list
- Remove favorites

### User Profiles
- Public user profiles
- Personal profile management

### API Features
- JWT Authentication
- Pagination
- Filtering
- Search
- Ordering
- Swagger/OpenAPI documentation

---

## Tech Stack

### Backend
- Python 3.11
- Django
- Django REST Framework

### Database
- PostgreSQL

### Authentication
- JWT (SimpleJWT)

### Documentation
- drf-spectacular
- Swagger UI

### Containerization
- Docker
- Docker Compose

### Testing
- Django Test Framework
- DRF APITestCase

---

## Project Structure

text users/ experiences/ participations/ reviews/ comments/ ride_offers/ favorites/ 

---

## Running Locally

### 1. Clone repository

bash git clone <repository-url> cd venturo-api 

### 2. Start Docker containers

bash docker compose up --build 

### 3. Run migrations

bash docker compose exec web python manage.py migrate 

### 4. Create superuser (optional)

bash docker compose exec web python manage.py createsuperuser 

### 5. Open API

text http://localhost:8000 

### 6. Open Swagger documentation

text http://localhost:8000/api/docs/ 

---

## Authentication

Obtain access and refresh tokens:

http POST /api/token/ 

Refresh token:

http POST /api/token/refresh/ 

Include access token in requests:

http Authorization: Bearer <access_token> 

---

## Testing

Run all tests:

bash python manage.py test 

Run tests for a specific app:

bash python manage.py test experiences python manage.py test reviews python manage.py test comments 

---

## Future Improvements

- Elasticsearch integration
- Real-time chat
- Notifications
- Experience recommendations
- Activity feeds
- Frontend application
- Mobile application

---

## Author

Sanja Mandic
