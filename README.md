# HostelDesk 🏢

HostelDesk is a premium, modern student complaint management web application built from scratch to streamline how hostel issues (maintenance, electrical, plumbing, etc.) are reported, upvoted, discussed, and resolved.

I designed this project to solve a real-world problem: replacing unstructured group chats or paper forms with an organized, visual dashboard where students can collaborate on resolving shared problems.

---

## 🚀 Key Features

* **🎨 Premium Glassmorphism UI:** Built with custom, modern CSS featuring dark-mode styling, smooth hover effects, micro-animations, and glassmorphic card designs.
* **📊 Analytics Dashboard:** A live stats section displaying Total Complaints, Pending Tasks, Resolution Rate (%), and Average Satisfaction Score.
* **👍 Intelligent Session-Based Upvoting:** Students can upvote issues to show urgency. The upvoting logic is constrained to one upvote per user per post using Django session tracking (no duplicate voting).
* **💬 Threaded Remarks:** Instead of multiple duplicate complaints, students can click into any complaint and reply/remark on a single thread.
* **🚨 3-Day Overdue Tracker:** An automated server-side check flags complaints that have been unresolved for more than 3 days with a pulsing red "OVERDUE" badge.
* **⭐ Interactive Satisfaction Rating:** Once an admin resolves a complaint, students can rate the quality of the resolution using an interactive star-rating component (1-5 stars).
* **🔍 Live Filter & Search:** Easily filter complaints by Status (Pending, In Progress, Resolved), Priority (High, Medium, Low), or search by student name and title.

---

## 🛠️ Technology Stack

* **Backend:** Python, Django
* **Database:** SQLite
* **Frontend:** Semantic HTML5, Custom CSS3 (Vanilla design tokens, responsive flexbox/grid layouts), JavaScript (ratings, animations)
* **Auth/Sessions:** Django Session Framework (used for upvote isolation)

---

## 📂 Database Architecture (Models)

I designed a relational database schema containing two primary models with a **One-to-Many** relationship:

1. **`Complaint`:** Stores the main complaint details, category, priority, status, upvote count, created/resolved timestamps, and the user's satisfaction rating.
2. **`Remark`:** Linked to `Complaint` via a `ForeignKey` (with `on_delete=models.CASCADE`). Each remark represents an individual student's comment in the thread.

---

## 🔧 Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/YuSiVi/HostelDesk.git
   cd HostelDesk
   ```

2. **Set up a Virtual Environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. **Install Django:**
   ```bash
   pip install django
   ```

4. **Run Migrations:**
   ```bash
   python manage.py migrate
   ```

5. **Start the Development Server:**
   ```bash
   python manage.py runserver
   ```
   Open `http://127.0.0.1:8000/` in your browser.
