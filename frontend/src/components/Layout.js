import React from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import {
  AppBar,
  Toolbar,
  Typography,
  Button,
  Box,
  Container,
} from '@mui/material';
import { useAuth } from '../context/AuthContext';

function Layout({ children }) {
  const { logout } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <Box>
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            Medical Insurance System
          </Typography>
          <Button
            color="inherit"
            onClick={() => navigate('/')}
            sx={{ mr: 1 }}
          >
            Dashboard
          </Button>
          <Button
            color="inherit"
            onClick={() => navigate('/patients')}
            sx={{ mr: 1 }}
          >
            Patients
          </Button>
          <Button
            color="inherit"
            onClick={() => navigate('/predictions')}
            sx={{ mr: 1 }}
          >
            Predictions
          </Button>
          <Button color="inherit" onClick={handleLogout}>
            Logout
          </Button>
        </Toolbar>
      </AppBar>
      <Container sx={{ mt: 4, mb: 4 }}>
        {children}
      </Container>
    </Box>
  );
}

export default Layout;

