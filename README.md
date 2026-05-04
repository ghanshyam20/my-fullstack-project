<h1 align="center">InsightHub</h1>
<p align="center">
  Subscription-Based Content Platform
</p>

<hr/>

<h2>1. Project Overview</h2>

<p>
InsightHub is a full-stack web application designed to deliver technical content through a subscription-based model.
The platform allows users to explore free content while restricting premium content behind a paid subscription.
</p>

<p>
The idea behind the system was to simulate a real-world SaaS product, where content creators (writers) publish articles,
and users consume content based on access levels.
</p>

<p><strong>Main capabilities include:</strong></p>

<ul>
  <li>Secure user authentication with OTP verification</li>
  <li>Role-based access (client and writer)</li>
  <li>Premium subscription system</li>
  <li>Payment integration using PayPal</li>
  <li>Content management for writers</li>
  <li>GDPR-related privacy features</li>
</ul>

<hr/>

<h2>2. Purpose of the Project</h2>

<p>
The purpose of this project was to understand how a modern web application can be structured to handle real-world requirements.
</p>

<ul>
  <li>Monetizing digital content through subscriptions</li>
  <li>Implementing secure access control</li>
  <li>Integrating third-party APIs (PayPal)</li>
  <li>Managing user data responsibly</li>
</ul>

<p>
It also helped in understanding backend engineering concepts such as authentication flows, database design,
API validation, and deployment pipelines.
</p>

<hr/>

<h2>3. System Architecture</h2>

<p>The system follows Django's Model–View–Template (MVT) architecture.</p>

<h3>Application Structure</h3>

<ul>
  <li><strong>account</strong> – authentication, OTP, profile, GDPR</li>
  <li><strong>client</strong> – article browsing, interactions, subscriptions, payments</li>
  <li><strong>writer</strong> – article creation and management</li>
</ul>

<h3>Request Flow</h3>

<ol>
  <li>User sends request from browser</li>
  <li>Django view processes logic</li>
  <li>Models interact with database</li>
  <li>Template renders response</li>
</ol>

<p>
This separation helped keep the system organized and easier to maintain.
</p>

<hr/>

<h2>4. Core Features</h2>

<h3>Authentication</h3>
<ul>
  <li>Email-based login</li>
  <li>OTP verification during registration</li>
  <li>Password reset using OTP</li>
  <li>Role-based redirection</li>
</ul>

<h3>Content Management</h3>
<ul>
  <li>Writers can create, update, and delete articles</li>
  <li>Articles can be free or premium</li>
  <li>Multiple images per article supported</li>
</ul>

<h3>Subscription System</h3>
<ul>
  <li>One-to-one relation between user and subscription</li>
  <li>Access controlled from backend</li>
  <li>Expiry-based validation</li>
</ul>

<h3>Payment</h3>
<ul>
  <li>PayPal integration (sandbox)</li>
  <li>Backend verification before activation</li>
  <li>Duplicate payment protection</li>
</ul>

<h3>User Interaction</h3>
<ul>
  <li>Like / Bookmark system</li>
  <li>Comment system (with replies)</li>
  <li>Report functionality</li>
  <li>Notification system</li>
</ul>

<hr/>

<h2>5. Backend Logic Implementation</h2>

<h3>Search System</h3>

<p>
Search is implemented using Django ORM. The query is split into terms and matched against title and content.
Title matches are given higher priority than content matches to improve relevance.
</p>

<h3>Access Control</h3>

<p>
Premium access is strictly handled in backend logic. Even if someone tries to bypass frontend,
the system checks subscription validity before returning content.
</p>

<h3>Premium Protection</h3>

<ul>
  <li>Backend flag (<code>can_access</code>) controls visibility</li>
  <li>Images are served through protected endpoint</li>
</ul>

<pre>
/protected-image/&lt;id&gt;/
</pre>

<p>
This was important because direct media access was a real issue during development.
We fixed it by routing images through a secure view.
</p>

<h3>Payment Handling</h3>

<p>
Payments are verified using PayPal API before activating subscriptions.
We validate:
</p>

<ul>
  <li>Order ID</li>
  <li>Status</li>
  <li>Amount</li>
  <li>Currency</li>
</ul>

<h3>Race Condition Handling</h3>

<p>
Initially, duplicate payments were being processed.  
This was solved using database transactions and locking:
</p>

<pre>
transaction.atomic()
select_for_update()
</pre>

<p>
This ensures only one payment is processed at a time.
</p>

<h3>Database Optimization</h3>

<ul>
  <li><code>select_related()</code> for joins</li>
  <li><code>prefetch_related()</code> for reverse relations</li>
  <li><code>annotate()</code> for counts</li>
  <li>Indexes for faster queries</li>
</ul>

<hr/>

<h2>6. Database Design</h2>

<p>Main entities include:</p>

<ul>
  <li>CustomUser</li>
  <li>Article</li>
  <li>Subscription</li>
  <li>Payment</li>
  <li>Comment / Like / Bookmark</li>
</ul>

<h3>Key Decisions</h3>

<ul>
  <li>OneToOne for Subscription → one user, one plan</li>
  <li>Unique constraints → prevent duplicate likes/bookmarks</li>
  <li>Indexes → improve performance</li>
</ul>

<hr/>

<h2>7. GDPR & Privacy</h2>

<ul>
  <li>Cookie consent banner implemented</li>
  <li>User can export personal data (JSON)</li>
  <li>User can delete account</li>
  <li>Consent timestamp stored in database</li>
</ul>

<p>
While building this, one challenge was making sure data deletion actually removes related records.
This was handled using cascading deletes and controlled queries.
</p>

<hr/>

<h2>8. Deployment</h2>

<ul>
  <li>DigitalOcean hosting</li>
  <li>Gunicorn server</li>
  <li>Docker container</li>
  <li>PostgreSQL database</li>
  <li>DigitalOcean Spaces for media</li>
</ul>

<p>
Deployment issues included static files and media handling, which were solved using collectstatic and S3 configuration.
</p>

<hr/>

<h2>9. CI/CD Pipeline</h2>

<ul>
  <li>GitHub Actions workflow</li>
  <li>Django checks</li>
  <li>Migration validation</li>
  <li>Linting and security scan</li>
</ul>

<p>
This helped catch issues early before merging into main branch.
</p>

<hr/>

<h2>10. Installation</h2>

<pre>
git clone https://github.com/ghanshyam20/my-fullstack-project.git
cd my-fullstack-project

python -m venv venv
source venv/bin/activate

pip install -r requirements.txt

python manage.py migrate
python manage.py runserver
</pre>

<hr/>

<h2>11. Team Contribution</h2>

<ul>
  <li><strong>Ghan Bhattarai</strong> – full backend, payments, deployment</li>
  <li><strong>Asish Chaurasia</strong> – planning, UI feedback, testing</li>
  <li><strong>Taranand Yadav</strong> – documentation, testing</li>
</ul>

<hr/>

<h2>12. Challenges Faced</h2>

<ul>
  <li>Securing premium images → solved using protected endpoint</li>
  <li>Duplicate payment issue → solved using transactions</li>
  <li>Search performance → improved using ORM optimization</li>
  <li>Media storage in production → solved using DigitalOcean Spaces</li>
</ul>

<hr/>

<h2>13. Reflection</h2>

<p>
This project gave practical experience in building a real backend system.
The most valuable learning was understanding how small logic mistakes (like payment validation or access control)
can break the entire system if not handled properly.
</p>

<p>
We also learned how to structure a project, manage code using Git workflows, and deploy a working production system.
</p>

<hr/>

<h2>14. Conclusion</h2>

<p>
InsightHub demonstrates a complete subscription-based platform with authentication, payments, and secure content delivery.
The system reflects real-world backend design and provides a solid base for future improvements.
</p>