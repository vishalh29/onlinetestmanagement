


# FastAPI with Docker

## Running the Project

Follow these steps to run this project:

1. **Clone the Repository:**



2. **Navigate to the Project Directory:**

   ```

3. **Build and Run Docker Containers:**

   ```sh
   docker-compose up --build -d
   ```

4. **Verify Containers Are Running:**

   ```sh
   docker-compose ps
   ```

5. **Access the API Documentation:**

   Open your browser and go to:

   [http://localhost:8000/docs](http://localhost:8000/docs)

   This will provide access to the API for both admin and user functionalities.

6. **Initialize Test and Quiz Data:**

   Run the `loaddata.py` script to initialize test and quiz data:

   ```sh
   docker exec -it fastapiwithdocker-web-1 /bin/sh
   python loaddata.py
   exit
   ```

   Verify that the API has one test and ten quizzes created.

---

Feel free to adjust the text to fit any specific needs or additional details about your project.
