import React, { useState } from 'react';
import { TextField, Button, MenuItem, FormControl, InputLabel, Select, Container, Typography, Box, Checkbox, FormControlLabel, FormGroup, Grid, FormLabel } from '@mui/material';

function Setup() {
  const [age, setAge] = useState('');
  const [height, setHeight] = useState('');
  const [weight, setWeight] = useState('');
  const [sex, setSex] = useState('');
  const [bodyFat, setBodyFat] = useState('');
  const [goal, setGoal] = useState('');
  const [dietType, setDietType] = useState('');
  const [allergies, setAllergies] = useState<string[]>([]);
  const [cookingDuration, setCookingDuration] = useState('');
  const [dailyBudget, setDailyBudget] = useState('');
  const [mealTimes, setMealTimes] = useState({
    breakfast: '',
    snack1: '',
    lunch: '',
    snack2: '',
    dinner: ''
  });
  const [mealRepetition, setMealRepetition] = useState('');

  const handleAllergyChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const value = event.target.value;
    setAllergies((prev) =>
      prev.includes(value) ? prev.filter((allergy) => allergy !== value) : [...prev, value]
    );
  };

  const handleMealTimeChange = (event: React.ChangeEvent<{ name?: string; value: unknown }>) => {
    const { name, value } = event.target;
    setMealTimes((prev) => ({
      ...prev,
      [name as string]: value as string
    }));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    // Handle form submission
  };

  const generateTimeOptions = (start: number, end: number, meal_type: string) => {
    const options = [];
    if (meal_type === "snack") {
        options.push(<MenuItem key="none" value="none">No Snack</MenuItem>);
    }
    for (let i = start; i <= end; i += 0.5) {
      const hour = Math.floor(i);
      const minute = (i % 1) * 60;
      const time = `${hour.toString().padStart(2, '0')}:${minute.toString().padStart(2, '0')}`;
      options.push(<MenuItem key={time} value={time}>{time}</MenuItem>);
    }
    return options;
  };

  return (
    <Box sx={{mt: 4 }}>
      <Container maxWidth="sm">
        <Box sx={{ mt: 4, backgroundColor: 'white', p: 3, borderRadius: 2 }}>
          <Typography variant="h4" component="h2" gutterBottom>
            Set Up Your Profile
          </Typography>
          <form onSubmit={handleSubmit}>
            <TextField
              label="Age"
              variant="outlined"
              fullWidth
              margin="normal"
              value={age}
              onChange={(e) => setAge(e.target.value)}
            />
            <TextField
              label="Height (cm)"
              variant="outlined"
              fullWidth
              margin="normal"
              value={height}
              onChange={(e) => setHeight(e.target.value)}
            />
            <TextField
              label="Weight (kg)"
              variant="outlined"
              fullWidth
              margin="normal"
              value={weight}
              onChange={(e) => setWeight(e.target.value)}
            />
            <FormControl variant="outlined" fullWidth margin="normal">
              <InputLabel>Biological Sex</InputLabel>
              <Select
                value={sex}
                onChange={(e) => setSex(e.target.value)}
                label="Biological Sex"
              >
                <MenuItem value="female">Female</MenuItem>
                <MenuItem value="male">Male</MenuItem>
              </Select>
            </FormControl>
            <FormControl variant="outlined" fullWidth margin="normal">
              <InputLabel>Body Fat</InputLabel>
              <Select
                value={bodyFat}
                onChange={(e) => setBodyFat(e.target.value)}
                label="Body Fat"
              >
                <MenuItem value="low">Low</MenuItem>
                <MenuItem value="medium">Medium</MenuItem>
                <MenuItem value="high">High</MenuItem>
              </Select>
            </FormControl>
            <FormControl variant="outlined" fullWidth margin="normal">
              <InputLabel>Goal</InputLabel>
              <Select
                value={goal}
                onChange={(e) => setGoal(e.target.value)}
                label="Goal"
              >
                <MenuItem value="lose fat">Lose Fat</MenuItem>
                <MenuItem value="maintain weight">Maintain Weight</MenuItem>
                <MenuItem value="build muscle">Build Muscle</MenuItem>
              </Select>
            </FormControl>
            <FormControl variant="outlined" fullWidth margin="normal">
              <InputLabel>Diet Type</InputLabel>
              <Select
                value={dietType}
                onChange={(e) => setDietType(e.target.value)}
                label="Diet Type"
              >
                <MenuItem value="anything">Anything</MenuItem>
                <MenuItem value="pescetarian">Pescetarian</MenuItem>
                <MenuItem value="vegetarian">Vegetarian</MenuItem>
                <MenuItem value="vegan">Vegan</MenuItem>
                <MenuItem value="keto">Keto</MenuItem>
                <MenuItem value="paleo">Paleo</MenuItem>
              </Select>
            </FormControl>
            <FormControl component="fieldset" margin="normal">
              <Typography component="legend">Allergies</Typography>
              <FormGroup>
                <Grid container spacing={2}>
                  {['gluten', 'peanuts', 'eggs', 'fish', 'nuts', 'dairy', 'soy', 'shellfish'].map((allergy) => (
                    <Grid item xs={6} sm={4} md={3} key={allergy}>
                      <FormControlLabel
                        control={
                          <Checkbox
                            checked={allergies.includes(allergy)}
                            onChange={handleAllergyChange}
                            value={allergy}
                          />
                        }
                        label={allergy.charAt(0).toUpperCase() + allergy.slice(1)}
                      />
                    </Grid>
                  ))}
                </Grid>
              </FormGroup>
            </FormControl>
            <FormControl variant="outlined" fullWidth margin="normal">
              <InputLabel>Cooking Duration</InputLabel>
              <Select
                value={cookingDuration}
                onChange={(e) => setCookingDuration(e.target.value)}
                label="Cooking Duration"
              >
                <MenuItem value="10-30 minutes">10 - 30 minutes</MenuItem>
                <MenuItem value="30 minutes-1 hour">30 minutes - 1 hour</MenuItem>
                <MenuItem value="1-1.5 hours">1 - 1.5 hours</MenuItem>
                <MenuItem value="1.5-2 hours">1.5 - 2 hours</MenuItem>
                <MenuItem value="2+ hours">2+ hours</MenuItem>
              </Select>
            </FormControl>
            <TextField
              label="Daily Budget (€)"
              variant="outlined"
              fullWidth
              margin="normal"
              value={dailyBudget}
              onChange={(e) => setDailyBudget(e.target.value)}
            />
            <FormControl component="fieldset" fullWidth margin="normal">
              <FormLabel component="legend">Meal Times</FormLabel>
              <Grid container spacing={2}>
                <Grid item xs={6}>
                  <FormControl variant="outlined" fullWidth margin="normal">
                    <InputLabel>Breakfast</InputLabel>
                    <Select
                      value={mealTimes.breakfast}
                      onChange={handleMealTimeChange}
                      label="Breakfast"
                      name="breakfast"
                    >
                      {generateTimeOptions(6, 12, "")}
                    </Select>
                  </FormControl>
                </Grid>
                <Grid item xs={6}>
                  <FormControl variant="outlined" fullWidth margin="normal">
                    <InputLabel>Snack 1</InputLabel>
                    <Select
                      value={mealTimes.snack1}
                      onChange={handleMealTimeChange}
                      label="Snack 1"
                      name="snack1"
                    >
                      {generateTimeOptions(10, 12, "snack")}
                    </Select>
                  </FormControl>
                </Grid>
                <Grid item xs={6}>
                  <FormControl variant="outlined" fullWidth margin="normal">
                    <InputLabel>Lunch</InputLabel>
                    <Select
                      value={mealTimes.lunch}
                      onChange={handleMealTimeChange}
                      label="Lunch"
                      name="lunch"
                    >
                      {generateTimeOptions(12, 16, "")}
                    </Select>
                  </FormControl>
                </Grid>
                <Grid item xs={6}>
                  <FormControl variant="outlined" fullWidth margin="normal">
                    <InputLabel>Snack 2</InputLabel>
                    <Select
                      value={mealTimes.snack2}
                      onChange={handleMealTimeChange}
                      label="Snack 2"
                      name="snack2"
                    >
                      {generateTimeOptions(15, 18, "snack")}
                    </Select>
                  </FormControl>
                </Grid>
                <Grid item xs={6}>
                  <FormControl variant="outlined" fullWidth margin="normal">
                    <InputLabel>Dinner</InputLabel>
                    <Select
                      value={mealTimes.dinner}
                      onChange={handleMealTimeChange}
                      label="Dinner"
                      name="dinner"
                    >
                      {generateTimeOptions(18, 22, "")}
                    </Select>
                  </FormControl>
                </Grid>
              </Grid>
            </FormControl>
            
            <FormControl variant="outlined" fullWidth margin="normal">
              <InputLabel>Meal Repetition</InputLabel>
              <Select
                value={mealRepetition}
                onChange={(e) => setMealRepetition(e.target.value)}
                label="Meal Repetition"
              >
                <MenuItem value="none">No Repetition</MenuItem>
                <MenuItem value="repeatDinnerForNextLunch">Repeat Dinner for Next Day's Lunch</MenuItem>
                <MenuItem value="repeatLunchForSameDinner">Repeat Lunch for Same Day's Dinner</MenuItem>
              </Select>
            </FormControl>

            <Button type="submit" variant="contained" color="primary" fullWidth sx={{ mt: 2 }}>
              Submit
            </Button>
          </form>
        </Box>
      </Container>
    </Box>
  );
}

export default Setup;