from flask import Flask, request, jsonify
from faker import Faker
import sqlite3
import requests
import time

app = Flask(__name__)

fake = Faker('hr_HR')

# Connect to SQLite database
conn = sqlite3.connect('./data.db')
c = conn.cursor()

# Create a table in the SQLite database for media_types
c.execute('''CREATE TABLE IF NOT EXISTS media_types
             (MediaTypeId INTEGER PRIMARY KEY, Name NVARCHAR(120))''')

# Create a table in the SQLite database for genres
c.execute('''CREATE TABLE IF NOT EXISTS genres
             (GenreId INTEGER PRIMARY KEY, Name NVARCHAR(120))''')

# Create a table in the SQLite database for playlists
c.execute('''CREATE TABLE IF NOT EXISTS playlists
             (PlaylistId INTEGER PRIMARY KEY, Name NVARCHAR(120))''')

# Create a table in the SQLite database for playlist_track
c.execute('''CREATE TABLE IF NOT EXISTS playlist_track
             (PlaylistId INTEGER, TrackId INTEGER, PRIMARY KEY (PlaylistId, TrackId))''')

# Create a table in the SQLite database for tracks
c.execute('''CREATE TABLE IF NOT EXISTS tracks
             (TrackId INTEGER PRIMARY KEY, Name NVARCHAR(200), AlbumId INTEGER, MediaTypeId INTEGER, GenreId INTEGER, 
             Composer NVARCHAR(220), Milliseconds INTEGER, Bytes INTEGER, UnitPrice NUMERIC)''')

# Create a table in the SQLite database for artists
c.execute('''CREATE TABLE IF NOT EXISTS artists
             (ArtistId INTEGER PRIMARY KEY, Name NVARCHAR(120))''')

# Create a table in the SQLite database for invoices
c.execute('''CREATE TABLE IF NOT EXISTS invoices
             (InvoiceId INTEGER PRIMARY KEY, CustomerId INTEGER, InvoiceDate DATETIME, 
             BillingAddress NVARCHAR(255), BillingCity NVARCHAR(255), BillingState NVARCHAR(255), 
             BillingCountry NVARCHAR(255), BillingPostalCode NVARCHAR(10), Total NUMERIC)''')

# Create a table in the SQLite database for invoice_items
c.execute('''CREATE TABLE IF NOT EXISTS invoice_items
             (InvoiceItemId INTEGER PRIMARY KEY, InvoiceId INTEGER, TrackId INTEGER, UnitPrice NUMERIC, Quantity INTEGER)''')

# Create a table in the SQLite database for albums
c.execute('''CREATE TABLE IF NOT EXISTS albums
             (AlbumId INTEGER PRIMARY KEY, Title NVARCHAR(160), ArtistId INTEGER)''')

# Create a table in the SQLite database for customers
c.execute('''CREATE TABLE IF NOT EXISTS customers
             (CustomerId INTEGER PRIMARY KEY, FirstName NVARCHAR(40), LastName NVARCHAR(20), 
             Company NVARCHAR(80), Address NVARCHAR(70), City NVARCHAR(40), State NVARCHAR(40), 
             Country NVARCHAR(40), PostalCode NVARCHAR(10), Phone NVARCHAR(24), Fax NVARCHAR(24), 
             Email NVARCHAR(60), SupportRepId INTEGER)''')

# Create a table in the SQLite database for employees
c.execute('''CREATE TABLE IF NOT EXISTS employees
             (EmployeeId INTEGER PRIMARY KEY, LastName NVARCHAR(20), FirstName NVARCHAR(20), 
             Title NVARCHAR(30), ReportsTo INTEGER, BirthDate DATETIME, HireDate DATETIME, 
             Address NVARCHAR(70))''')

# Generate fake data if the media_types table is empty
c.execute("SELECT COUNT(*) FROM media_types")
count = c.fetchone()[0]
if count == 0:
    for _ in range(1000):
        c.execute("INSERT INTO media_types (Name) VALUES (?)", (fake.word(),))

# Generate fake data if the employees table is empty
c.execute("SELECT COUNT(*) FROM employees")
count = c.fetchone()[0]
if count == 0:
    for _ in range(1000):
        c.execute("INSERT INTO employees (LastName, FirstName, Title, ReportsTo, BirthDate, HireDate, Address) VALUES (?, ?, ?, ?, ?, ?, ?)",
                  (fake.last_name(), fake.first_name(), fake.word(), fake.random_int(min=1, max=100, step=1),
                   fake.date_of_birth(minimum_age=18, maximum_age=65).strftime('%Y-%m-%d'),
                   fake.date_this_decade().strftime('%Y-%m-%d'), fake.address()))

# Generate fake data if the customers table is empty
c.execute("SELECT COUNT(*) FROM customers")
count = c.fetchone()[0]
if count == 0:
    for _ in range(1000):
        c.execute("INSERT INTO customers (FirstName, LastName, Company, Address, City, State, Country, PostalCode, Phone, Fax, Email, SupportRepId) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                  (fake.first_name(), fake.last_name(), fake.company(), fake.address(), fake.city(),
                   fake.state(), fake.country(), fake.zip(), fake.phone_number(), fake.phone_number(), fake.email(),
                   fake.random_int(min=1, max=10, step=1)))

# Generate fake data if the invoices table is empty
c.execute("SELECT COUNT(*) FROM invoices")
count = c.fetchone()[0]
if count == 0:
    for _ in range(1000):
        c.execute("INSERT INTO invoices (CustomerId, InvoiceDate, BillingAddress, BillingCity, BillingState, BillingCountry, BillingPostalCode, Total) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                  (fake.random_int(min=1, max=100, step=1), fake.date_this_decade().strftime('%Y-%m-%d'),
                   fake.address(), fake.city(), fake.state(), fake.country(), fake.zip(), fake.random_int(min=1, max=100, step=1)))

# Generate fake data if the invoice_items table is empty
c.execute("SELECT COUNT(*) FROM invoice_items")
count = c.fetchone()[0]
if count == 0:
    for _ in range(1000):
        c.execute("INSERT INTO invoice_items (InvoiceId, TrackId, UnitPrice, Quantity) VALUES (?, ?, ?, ?)",
                  (fake.random_int(min=1, max=100, step=1), fake.random_int(min=1, max=100, step=1),
                   fake.random_int(min=1, max=20, step=1), fake.random_int(min=1, max=10, step=1)))

# Generate fake data if the artists table is empty
c.execute("SELECT COUNT(*) FROM artists")
count = c.fetchone()[0]
if count == 0:
    for _ in range(1000):
        c.execute("INSERT INTO artists (Name) VALUES (?)", (fake.name(),))

# Generate fake data if the albums table is empty
c.execute("SELECT COUNT(*) FROM albums")
count = c.fetchone()[0]
if count == 0:
    for _ in range(1000):
        c.execute("INSERT INTO albums (Title, ArtistId) VALUES (?, ?)",
                  (fake.word(), fake.random_int(min=1, max=100, step=1)))

# Generate fake data if the media_types table is empty
c.execute("SELECT COUNT(*) FROM media_types")
count = c.fetchone()[0]
if count == 0:
    for _ in range(1000):
        c.execute("INSERT INTO media_types (Name) VALUES (?)", (fake.word(),))

# Generate fake data if the genres table is empty
c.execute("SELECT COUNT(*) FROM genres")
count = c.fetchone()[0]
if count == 0:
    for _ in range(1000):
        c.execute("INSERT INTO genres (Name) VALUES (?)", (fake.word(),))

# Generate fake data if the tracks table is empty
c.execute("SELECT COUNT(*) FROM tracks")
count = c.fetchone()[0]
if count == 0:
    for _ in range(1000):
        c.execute("INSERT INTO tracks (Name, AlbumId, MediaTypeId, GenreId, Composer, Milliseconds, Bytes, UnitPrice) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                  (fake.word(), fake.random_int(min=1, max=100, step=1),
                   fake.random_int(min=1, max=100, step=1), fake.random_int(min=1, max=100, step=1),
                   fake.name(), fake.random_int(min=10000, max=600000, step=10000), fake.random_int(min=100000, max=10000000, step=100000),
                   fake.random_int(min=1, max=20, step=1)))

# Generate fake data if the playlists table is empty
c.execute("SELECT COUNT(*) FROM playlists")
count = c.fetchone()[0]
if count == 0:
    for _ in range(1000):
        c.execute("INSERT INTO playlists (Name) VALUES (?)", (fake.word(),))

# Generate fake data if the playlist_track table is empty
c.execute("SELECT COUNT(*) FROM playlist_track")
count = c.fetchone()[0]
if count == 0:
    for _ in range(1000):
        playlist_id = fake.random_int(min=1, max=100, step=1)
        track_id = fake.random_int(min=1, max=100, step=1)

        # Check if the entry already exists
        if not c.execute("SELECT 1 FROM playlist_track WHERE PlaylistId=? AND TrackId=?", (playlist_id, track_id)).fetchone():
            c.execute("INSERT INTO playlist_track (PlaylistId, TrackId) VALUES (?, ?)",
                      (playlist_id, track_id))

# Commit the transaction
conn.commit()

# Close the connection
conn.close()

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/query', methods=['POST'])
def run_query():
    query = request.json['query']
    with sqlite3.connect('./data.db') as conn:
        cursor = conn.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
    return jsonify(results)

@app.route('/send_query', methods=['GET'])
def send_query():
    # Define the URL of your Flask application
    url = 'http://localhost:8000/query'

    # Define the query you want to send
    query = """
    SELECT
        tracks.albumid AlbumId,
        Title,
        SUM(milliseconds) AS TotalMilliseconds
    FROM
        tracks
    INNER JOIN albums ON albums.albumid = tracks.albumid
    GROUP BY
        tracks.albumid, 
        title
    HAVING
        SUM(milliseconds) > 1000000
    ORDER BY
        TotalMilliseconds DESC;
    """

    # Create a JSON payload with the query
    payload = {'query': query}

    # Record the start time
    start_time = time.time()
    
    # Send the POST request
    response = requests.post(url, json=payload)

    # Record the end time
    end_time = time.time()

    # Calculate the time needed to make the query
    time_taken = end_time - start_time

    # Print the response
    print(f"Query sent successfully.")
    print(f"Time taken to make the query: {time_taken} seconds.")
    print(response.status_code)
    return response.json()

if __name__ == '__main__':
    app.run(debug=True)
