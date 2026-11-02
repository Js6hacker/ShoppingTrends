// src/App.js
import React, { useState } from 'react';
import './App.css';

function App() {
  const [formData, setFormData] = useState({
    Age: '',
    Gender: 'Male',
    Category: 'Clothing',
    Size: 'M',
    Season: 'Summer',
  });

  const [result, setResult] = useState('');

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setResult('Predicting...');

    try {
      const response = await fetch('http://localhost:5000/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData),
      });

      const data = await response.json();
      if (data['predicted_item']) {
        setResult(`Predicted Item: ${data['predicted_item']}`);
      } else {
        setResult(`Error: ${data.error}`);
      }
    } catch (error) {
      setResult(`Request failed: ${error.message}`);
    }
  };

  return (
    <div className="App">
      <h1>Item Purchase Predictor</h1>
      <form onSubmit={handleSubmit}>
        <label>Age:</label>
        <input type="number" name="Age" value={formData.Age} onChange={handleChange} required />

        <label>Gender:</label>
        <select name="Gender" value={formData.Gender} onChange={handleChange}>
          <option>Male</option>
          <option>Female</option>
        </select>

        <label>Category:</label>
        <select name="Category" value={formData.Category} onChange={handleChange}>
          <option>Clothing</option>
          <option>Footwear</option>
          <option>Outerwear</option>
        </select>

        <label>Size:</label>
        <select name="Size" value={formData.Size} onChange={handleChange}>
          <option>S</option>
          <option>M</option>
          <option>L</option>
          <option>XL</option>
        </select>

        <label>Season:</label>
        <select name="Season" value={formData.Season} onChange={handleChange}>
          <option>Summer</option>
          <option>Winter</option>
          <option>Spring</option>
          <option>Fall</option>
        </select>

        <button type="submit">Predict</button>
      </form>

      <div className="result">{result}</div>
    </div>
  );
}

export default App;
