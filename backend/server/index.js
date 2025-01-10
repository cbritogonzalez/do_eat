const express = require('express');
const bodyParser = require('body-parser');
const { Pool } = require('pg');
const cors = require('cors'); // Import the cors package

const app = express();
const port = 3000;

// PostgreSQL connection pool
const pool = new Pool({
  user: 'postgres',
  host: 'localhost',
  database: 'postgres',
  password: '1234',
  port: 5432,
});

app.use(bodyParser.json());
app.use(cors()); // Enable CORS (To allow the front end to communicate with the backend)

app.post('/saveProfile', async (req, res) => {
  const {age, allergies, bodyFat, budget, cookingDuration, dietType, goal, height, mealRepetition, mealTimes, sex, weight} = req.body;

  if (!age || !height || !weight || !budget || !sex || !bodyFat || !goal || !dietType || !allergies || !cookingDuration || !mealTimes || !mealRepetition) {
    return res.status(400).send('All fields are required');
  }

  try {
    const query = "CALL insert_user($1::smallint, $2::TEXT[], $3::TEXT, $4::money, $5::TEXT, $6::TEXT, $7::TEXT, $8::smallint, $9::text, $10::time, $11::time, $12::time, $13::time, $14::time, $15::TEXT, $16::smallint)";
    const values = [age, allergies, bodyFat, budget, cookingDuration, dietType, goal, height, mealRepetition, mealTimes.breakfast, mealTimes.snack1, mealTimes.lunch, mealTimes.snack2, mealTimes.dinner, sex, weight];
    await pool.query(query, values);
    res.status(201).send('Profile saved successfully');
  } catch (err) {
    console.error(err);
    res.status(500).send('Server error');
  }
});

app.listen(port, () => {
  console.log(`Server running on port ${port}`);
});