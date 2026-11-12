# Gregorian to Hebrew Date Converter

A lightweight full-stack integration service and web application that converts Gregorian dates into Hebrew dates using the external **Hebcal REST API**.

## Features

* **Gregorian-to-Hebrew Conversion:** Integrates with the Hebcal `/converter` REST endpoint (`g2h=1`, `strict=1`) to return accurate Hebrew dates.

* **Hebrew Day Boundary Support (Sunset Toggle):** Includes an *After sunset* option (`gs=on`) to account for the Hebrew calendar day starting at sunset.

* **Dual-Layer Input Validation:** Enforces date format (`YYYY-MM-DD`) and a dynamic year range (`±200` years from the current year) on both the frontend (UX) and backend (data integrity).

* **Normalized API Contract:** Transforms the external API payload into a clean, deterministic JSON response with unambiguous Gregorian date formatting (`DD/MM/YYYY (Month DD, YYYY)`) and strips unrequested liturgical metadata.

* **Resilient Error Handling:** Implements request timeouts (`5s`) and maps upstream or client failures to standard HTTP status codes (`200`, `400`, `502`, `504`).

* **Clean Architecture:** Separates backend integration logic (`Flask`) from frontend structure (`HTML`), styling (`CSS`), and client-side behavior (`JavaScript`).

## Project Structure

```
gregorian-to-hebrew-converter/
├── app.py                  # Flask backend & Hebcal REST API integration service
├── requirements.txt        # Python dependencies
├── README.md               # Project documentation
├── templates/
│   └── index.html          # Main UI markup
└── static/
    ├── css/
    │   └── styling.css     # Component styling & visibility utility classes
    └── js/
        └── script.js       # Asynchronous fetch logic, dynamic bounds & UI state

```

## Prerequisites

* **Python 3.8+**

* **pip** (Python package manager)

## Installation & Usage

1. **Clone the repository:**

   ```
   git clone <YOUR_GITHUB_REPOSITORY_URL>
   cd <REPOSITORY_FOLDER_NAME>
   
   ```

2. **Install dependencies:**

   ```
   pip install -r requirements.txt
   
   ```

3. **Run the application:**

   ```
   python app.py
   
   ```

4. **Open in browser:**
   Navigate to `http://127.0.0.1:5000`

## API Endpoint Documentation

### `POST /api/convert`

Converts a given Gregorian date to its corresponding Hebrew date.

**Request Body (`application/json`):**

```
{
  "date": "2026-12-10",
  "after_sunset": false
}

```

**Success Response (`200 OK`):**

```
{
  "gregorian_date": "10/12/2026 (December 10, 2026)",
  "hebrew_date": "ל׳ בְּכִסְלֵו תשפ״ז"
}

```

**HTTP Status Codes:**

* `200 OK` – Date converted successfully.

* `400 Bad Request` – Missing date, invalid format, or year outside the allowed `±200` year range.

* `502 Bad Gateway` – Upstream communication error with the Hebcal API.

* `504 Gateway Timeout` – Hebcal API request exceeded the 5-second timeout.