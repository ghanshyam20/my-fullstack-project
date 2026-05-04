InsightHub – Subscription-Based Content Platform

1. Project Overview

InsightHub is a full-stack web application designed to deliver technical content through a subscription-based model. The platform allows users to explore free content while restricting premium content behind a paid subscription.

The system simulates a real-world SaaS product where content creators (writers) publish articles and users consume content based on access levels.

The platform supports:

Secure user authentication with OTP verification
Role-based access (client and writer)
Premium subscription system
Payment integration with PayPal
Content management for writers
GDPR-related privacy features


2. Purpose of the Project

The main purpose of this project is to demonstrate how a modern web application can be designed to:

Monetize digital content
Enforce access control securely
Integrate third-party payment systems
Maintain user data privacy and compliance

This project also reflects real-world backend engineering practices including authentication, database design, API integration, and deployment.

3. System Architecture

The system follows the Django MVT (Model–View–Template) architecture.

Application Structure

The project is divided into three main applications:

account
Handles authentication, OTP verification, user profile, GDPR features
client
Handles article browsing, interactions (like, comment, bookmark), subscriptions, payments
writer
Handles article creation, editing, and management



Request Flow
User sends request (browser)
Django view processes logic
Models interact with database
Template renders response

This separation ensures maintainability and scalability.


4. Core Features
Authentication System
Email-based login
OTP verification for account activation
Password reset with OTP
Role-based redirection (writer vs client)
Content System
Writers can create, update, and delete articles
Articles can be marked as free or premium
Multiple images per article supported
Subscription System
One-to-one relationship between user and subscription
Premium access controlled via backend validation
Subscription expiry handling
Payment Integration
PayPal API (sandbox)
Backend verification of transactions
Duplicate payment prevention
User Interaction
Like system (toggle)
Bookmark system
Comment system (with replies)
Report system
Notification system
5. Backend Logic Implementation
Search Functionality

The search system is implemented using Django ORM with dynamic query building.

Input query is split into terms
Each term is matched against:
article title
article content
Results are ranked using conditional logic:
Title matches have higher priority than content matches

This improves search relevance without requiring external search engines.

Subscription and Access Control

Access to premium content is strictly controlled by backend logic.

Each user has a subscription object, and access is validated using:

Subscription plan
Active status
Expiration date

If conditions are not met, access is restricted.

Premium Content Protection

Premium content is protected at multiple levels:

1. Backend Access Control

The system uses a boolean flag (can_access) to determine access.

2. Media Protection

Images are not directly exposed. Instead, they are served through a protected endpoint:

/protected-image/<id>/

Unauthorized users receive a forbidden response.

3. Frontend Restriction
Only preview content is shown
Limited number of images displayed
Full content unlocked only after subscription
Payment System

The payment flow is implemented using PayPal API and includes:

Order creation
Payment capture
Validation of:
order ID
payment status
amount
currency

Only verified payments activate subscriptions.

Race Condition Handling

To prevent duplicate transactions, the system uses database-level locking:

Atomic transactions
select_for_update() for payment validation

This ensures consistency even under concurrent requests.

Database Optimization

The system uses several optimization techniques:

select_related() for foreign key joins
prefetch_related() for reverse relations
annotate() for aggregated values (likes, views)
Indexing for frequently queried fields

These techniques improve performance and reduce database load.

6. Database Design

The system includes the following key entities:

CustomUser (authentication)
Article (content)
ArticleImage (media)
Subscription (access control)
Payment (transactions)
Comment (user interaction)
Like, Bookmark (engagement)
Notification (activity tracking)
Design Decisions
OneToOne (Subscription)
Ensures each user has a single subscription
Unique Constraints (Like, Bookmark)
Prevent duplicate interactions
Indexes
Improve performance for search and filtering
7. GDPR and Privacy Features

The system includes basic GDPR-compliant features:

Cookie Consent
Cookie banner displayed on first visit
User consent required before usage
Data Protection
Users can export personal data in JSON format
Users can delete their account permanently
Transparency
Privacy Policy and Terms pages included
Users are informed about:
data usage
email communication
subscription handling
Security
Passwords are hashed
OTP-based verification ensures secure onboarding
8. Deployment

The application is deployed using:

DigitalOcean (hosting)
Gunicorn (application server)
Docker (containerization)
PostgreSQL (production database)
DigitalOcean Spaces (media storage)

Static files are handled using Django's collectstatic process.

9. CI/CD Pipeline

The project uses GitHub Actions for continuous integration.

Pipeline includes:

Code checkout
Dependency installation
Django system checks
Migration validation
Linting (flake8)
Security scanning (bandit)

This ensures code quality and consistency before merging.

10. Installation Guide
Step 1: Clone Repository
git clone https://github.com/ghanshyam20/my-fullstack-project.git
Step 2: Setup Environment
python -m venv venv
source venv/bin/activate
Step 3: Install Dependencies
pip install -r requirements.txt
Step 4: Run Migrations
python manage.py migrate
Step 5: Start Server
python manage.py runserver
11. Team Contribution
Ghan Bhattarai
Full backend development
Payment system integration
Authentication system
Deployment and CI/CD
Asish Chaurasia
Project planning
UI feedback
Testing support
Taranand Yadav
Documentation
Testing and validation
12. Limitations
Search system is basic (no advanced ranking engine)
UI/UX can be further improved
No recommendation system implemented
Limited analytics features
13. Reflection

This project provided hands-on experience in building a real-world web application.

Key learnings include:

Designing scalable backend systems
Implementing secure authentication
Handling payments and subscriptions
Managing database performance
Deploying production-ready applications

The most challenging part was ensuring secure premium content access and handling payment validation correctly.

14. Conclusion

InsightHub demonstrates a complete content subscription system with authentication, payment integration, and secure access control. The project reflects real-world engineering practices and provides a strong foundation for further development.