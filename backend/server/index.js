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
  database: 'do_eat_db',
  password: '1234',
  port: 5432,
});

app.use(bodyParser.json());
app.use(cors()); // Enable CORS (To allow the front end to communicate with the backend)

app.post('/saveProfile', async (req, res) => {
  const {email, age, allergies, bodyFat, budget, cookingDuration, dietType, goal, height, mealRepetition, mealTimes, sex, weight} = req.body;

  if (!age || !height || !weight || !budget || !sex || !bodyFat || !goal || !dietType || !allergies || !cookingDuration || !mealTimes || !mealRepetition) {
    return res.status(400).send('All fields are required');
  }

  try {
    console.log(email);
    const query = "CALL insert_user($17::TEXT, $1::smallint, $2::TEXT[], $3::TEXT, $4::money, $5::TEXT, $6::TEXT, $7::TEXT, $8::smallint, $9::text, $10::time, $11::time, $12::time, $13::time, $14::time, $15::TEXT, $16::smallint)";
    const values = [age, allergies, bodyFat, budget, cookingDuration, dietType, goal, height, mealRepetition, mealTimes.breakfast, mealTimes.snack1, mealTimes.lunch, mealTimes.snack2, mealTimes.dinner, sex, weight, email];
    await pool.query(query, values);
    res.status(201).send('Profile saved successfully');
  } catch (err) {
    console.error(err);
    res.status(500).send('Server error');
  }
});

app.post('/createMeals', async (req, res) => {
  try {
    const queryParams = req.query;
    const email = queryParams.email;
    const response = await fetch('http://localhost:8000/nutrition/user/recipes/?email=' + email, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      }
    });
    const data = await response.json();
    res.status(201).json(data);
  } catch (error) {
    console.error('Error calling external endpoint:', error);
    res.status(500).json({ error: 'Internal Server Error' });
  }
});

app.get('/scheduledMeals', async (req, res) => {
  const queryParams = req.query;
  const email = queryParams.email;


  if (!email) {
    return res.status(400).json({ error: 'email is required' });
  }

  try {
    const client = await pool.connect();
    const email_result = await client.query(
      `SELECT user_id FROM users WHERE email = $1 LIMIT 1`,
      [email]
    );
    const userId = email_result.rows[0].user_id;
    console.log('userId', userId);
    const result = await client.query(
      `SELECT * FROM get_scheduled_meals($1)`,
      [userId]
    );
    console.log('from index.js', result.rows);
    client.release();
    res.status(200).json(result.rows);
  } catch (error) {
    console.error('Error fetching scheduled meals:', error);
    res.status(500).json({ error: 'Internal Server Error' });
  }
});

app.listen(port, () => {
  console.log(`Server running on port ${port}`);
});