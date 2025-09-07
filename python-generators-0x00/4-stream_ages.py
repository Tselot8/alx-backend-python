#!/usr/bin/python3
seed = __import__('seed')

# ---------------- Generator: stream user ages ---------------- #
def stream_user_ages():
    """Yields user ages one by one from the database."""
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT age FROM user_data;")
    
    for row in cursor:  # ✅ loop 1
        yield row['age']

    cursor.close()
    connection.close()


# ---------------- Compute average age ---------------- #
def average_age():
    """Calculates the average age using the generator without loading all data."""
    total = 0
    count = 0
    for age in stream_user_ages():  # ✅ loop 2
        total += age
        count += 1

    if count == 0:
        return 0
    return total / count


if __name__ == "__main__":
    avg = average_age()
    print(f"Average age of users: {avg}")
