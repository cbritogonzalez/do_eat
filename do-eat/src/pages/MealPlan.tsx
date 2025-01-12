import React, { useEffect, useState } from 'react';
import Layout from '../components/Layout';
import './MealPlan.css';

const getCookie = (name) => {
  const cookieString = document.cookie;
  const cookies = cookieString.split("; ");
  for (let cookie of cookies) {
      const [key, value] = cookie.split("=");
      if (key === name) return decodeURIComponent(value);
  }
  return null; // Return null if the cookie is not found
};

const fetchScheduledMeals = async (email) => {
  const response = await fetch(`http://localhost:3000/scheduledMeals?email=${email}`);
  console.log('fetchScheduledMeals response:', response); // Add this line
  const data = await response.json();
  return data;
};

function MealPlan() {
  const [mealPlan, setMealPlan] = useState([]);

  useEffect(() => {
    const email = getCookie("email")?.replace(/"/g, "");
    fetchScheduledMeals(email).then(data => setMealPlan(data));
  }, []);

  return (
    <Layout>
      {mealPlan.map((meal, index) => (
        <div key={index} className="meal">
          <h1 className="meal-time">
            {new Date(meal.date_time).toLocaleDateString('en-US', {
              weekday: 'long',
              day: 'numeric',
              month: 'long',
              hour: '2-digit',
              minute: '2-digit'
            })}
          </h1>
          <h3 className="meal-title">{meal.recipe_name}</h3>
          <p className="meal-nutrition green-text">{meal.nutrition_info}</p>
          <p className="meal-cook-time"><span className="icon-clock"></span> <strong>Cook Time:</strong> {meal.total_cook_time}</p>
          <p className="meal-cost"><span className="icon-money"></span> <strong>Cost:</strong> {meal.cost}</p>
          <p className="meal-portions"><span className="icon-human"></span> <strong>Portions:</strong> {meal.portions}</p>
          <ul className="meal-ingredients">
            {meal.ingredients.split(', ').map((ingredient, index) => (
              <li key={index}>{ingredient}</li>
            ))}
          </ul>
          <p className="meal-description"><strong>Instructions:</strong></p>
          <p className="meal-description">{meal.instructions}</p>
        </div>
      ))}
    </Layout>
  );
}

export default MealPlan;