import React from 'react';
import { Container, Typography, Box, Grid, Card, CardContent } from '@mui/material';
import { useAuth } from '../context/AuthContext';
import Layout from '../components/Layout';

function Dashboard() {
  const { user } = useAuth();

  return (
    <Layout>
      <Container>
        <Typography variant="h4" gutterBottom>
          Dashboard
        </Typography>
        <Typography variant="body1" color="textSecondary" gutterBottom>
          Welcome to the Federated Medical Insurance Cost Prediction System
        </Typography>

        <Grid container spacing={3} sx={{ mt: 2 }}>
          <Grid item xs={12} md={4}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Patients
                </Typography>
                <Typography variant="body2" color="textSecondary">
                  Manage patient records and view patient data
                </Typography>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} md={4}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Predictions
                </Typography>
                <Typography variant="body2" color="textSecondary">
                  Get insurance cost predictions for patients
                </Typography>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} md={4}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Model Status
                </Typography>
                <Typography variant="body2" color="textSecondary">
                  View federated learning model status and metrics
                </Typography>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      </Container>
    </Layout>
  );
}

export default Dashboard;

