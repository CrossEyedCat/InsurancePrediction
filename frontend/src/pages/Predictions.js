import React, { useState } from 'react';
import {
  Container,
  Typography,
  Paper,
  TextField,
  Button,
  Box,
  Grid,
  Alert,
} from '@mui/material';
import Layout from '../components/Layout';
import axios from 'axios';

function Predictions() {
  const [formData, setFormData] = useState({
    age: '',
    sex: 'male',
    bmi: '',
    children: 0,
    smoker: 'no',
    region: 'northeast',
  });
  const [prediction, setPrediction] = useState(null);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setPrediction(null);

    try {
      const response = await axios.post('/api/predictions', formData);
      setPrediction(response.data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Prediction failed');
    }
  };

  return (
    <Layout>
      <Container>
        <Typography variant="h4" gutterBottom>
          Insurance Cost Prediction
        </Typography>

        <Grid container spacing={3}>
          <Grid item xs={12} md={6}>
            <Paper sx={{ p: 3 }}>
              <Typography variant="h6" gutterBottom>
                Patient Information
              </Typography>
              <form onSubmit={handleSubmit}>
                <TextField
                  fullWidth
                  margin="normal"
                  label="Age"
                  type="number"
                  required
                  value={formData.age}
                  onChange={(e) => setFormData({ ...formData, age: e.target.value })}
                />
                <TextField
                  fullWidth
                  margin="normal"
                  select
                  label="Sex"
                  value={formData.sex}
                  onChange={(e) => setFormData({ ...formData, sex: e.target.value })}
                  SelectProps={{ native: true }}
                >
                  <option value="male">Male</option>
                  <option value="female">Female</option>
                </TextField>
                <TextField
                  fullWidth
                  margin="normal"
                  label="BMI"
                  type="number"
                  value={formData.bmi}
                  onChange={(e) => setFormData({ ...formData, bmi: e.target.value })}
                />
                <TextField
                  fullWidth
                  margin="normal"
                  label="Children"
                  type="number"
                  value={formData.children}
                  onChange={(e) => setFormData({ ...formData, children: e.target.value })}
                />
                <TextField
                  fullWidth
                  margin="normal"
                  select
                  label="Smoker"
                  value={formData.smoker}
                  onChange={(e) => setFormData({ ...formData, smoker: e.target.value })}
                  SelectProps={{ native: true }}
                >
                  <option value="no">No</option>
                  <option value="yes">Yes</option>
                </TextField>
                <Button
                  type="submit"
                  variant="contained"
                  fullWidth
                  sx={{ mt: 2 }}
                >
                  Predict Cost
                </Button>
              </form>
            </Paper>
          </Grid>

          <Grid item xs={12} md={6}>
            <Paper sx={{ p: 3 }}>
              <Typography variant="h6" gutterBottom>
                Prediction Result
              </Typography>
              {error && <Alert severity="error">{error}</Alert>}
              {prediction && (
                <Box>
                  <Typography variant="h4" color="primary">
                    ${parseFloat(prediction.predicted_cost).toFixed(2)}
                  </Typography>
                  <Typography variant="body2" color="textSecondary" sx={{ mt: 1 }}>
                    Model Version: {prediction.model_version || 'N/A'}
                  </Typography>
                </Box>
              )}
            </Paper>
          </Grid>
        </Grid>
      </Container>
    </Layout>
  );
}

export default Predictions;

