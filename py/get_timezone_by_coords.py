"""
|--------------------------------------------------------------------------
| Get timezone name by coordinates
|--------------------------------------------------------------------------
| Uses an API to get timezone by latitude and longitude.
"""
import json
import requests
import mysql.connector
import time
import timeit

# define key
api_key = "" # put API key here
file_name = "update-loc-tz.sql"

# Database connection function
def db_connect():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="r00tr00t",
        db="iso",
        connection_timeout=600,
        autocommit=True
    )

id_start = 23158 # 5276
max_chunks = 2500

# Generator to fetch data in chunks
def get_all_coords(chunk_size=max_chunks):
    db = db_connect()
    cur = db.cursor()

    sql_query = f"""
SELECT id, latitude as lat, longitude as lon
from location
where timezone_id is null and status = 1 and latitude is not null and longitude is not null order by id desc
"""

    cur.execute(sql_query)

    while True:
        rows = cur.fetchmany(chunk_size)
        if not rows:
            break
        yield rows  # Yield chunk instead of storing everything in memory

    cur.close()
    db.close()


# Function to get timezone name for given coordinates
def fetch_tz_name_by_coords(lat, lon):
    url = f"http://vip.timezonedb.com/v2.1/get-time-zone?key={api_key}&format=json&fields=zoneName&by=position&lat={lat}&lng={lon}"

    try:
        response = requests.get(url)

        # Check if the response is empty
        if response.status_code != 200:
            print(f"⚠️ API Error: {response.status_code} for lat={lat}, lon={lon}")
            return None

        # Check if response content is empty
        if not response.text.strip():
            print(f"⚠️ Empty response from API for lat={lat}, lon={lon}")
            return None

        # Try to parse JSON
        data = response.json()

        # Handle API errors
        if "zoneName" not in data:
            print(f"⚠️ Unexpected API response: {data}")
            return None

        # Check for Argentina exception
        if "America/Argentina/" in data["zoneName"]:
            return "America/Buenos_Aires"

        return data["zoneName"]

    except requests.exceptions.RequestException as e:
        print(f"🚨 Network error: {e}")
        return None
    except ValueError:
        print(f"🚨 JSON decoding error! Raw response: {response.text}")
        return None

# Function to write SQL update queries to file
def output_sql(lines):
    with open(file_name, 'a') as file:
        file.write("\n".join(lines))

    file.close()

def update_sql():
    sql = "UPDATE iso.location SET timezone_id = (SELECT id FROM timezone WHERE name = %s) WHERE id = %s;"
    cur.execute(sql, (tz_name, loc_id))
    cur.execute(sql)
    db.commit()


# MAIN PROCESS

start_time = time.time()
lines = []
request_count = 0
max_requests_per_minute = 2000  # Adjust based on API limits
pause_time = 5

db = db_connect()
cur = db.cursor()

for chunk in get_all_coords():
    for loc_id, lat, lon in chunk:

        tz_name = fetch_tz_name_by_coords(lat, lon)
        if tz_name:
            sql = f"UPDATE iso.location SET timezone_id = (SELECT id FROM timezone WHERE name = '{tz_name}') WHERE id = {loc_id};"
            print(sql)
            cur.execute(sql)
            db.commit()


        # Throttle requests to avoid API limits
        request_count += 1
        if request_count >= max_requests_per_minute:
            print(f'-- pausing for {pause_time} seconds...')
            time.sleep(pause_time)  # Pause for a minute
            request_count = 0

# Write all SQL updates to file
#output_sql(lines)
print(f"✅ {len(lines)} update statements written to {file_name}.")

end_time = time.time()
elapsed_time = end_time - start_time
time_str = timeit.timeit('1 + 1', number=1000000)
print(f"Time taken: {time_str:.6f} seconds")
print(f"Total seconds: {elapsed_time}")  # Get total time in seconds
