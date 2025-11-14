import React, { useState, useEffect } from 'react';
import {
  Container,
  Typography,
  Button,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  Box,
} from '@mui/material';
import AddIcon from '@mui/icons-material/Add';
import Layout from '../components/Layout';
import axios from 'axios';

function Patients() {
  const [patients, setPatients] = useState([]);
  const [open, setOpen] = useState(false);
  const [formData, setFormData] = useState({
    first_name: '',
    last_name: '',
    age: '',
    sex: 'male',
    bmi: '',
    children: 0,
    smoker: 'no',
    region: '',
  });

  useEffect(() => {
    fetchPatients();
  }, []);

  const fetchPatients = async () => {
    try {
      const response = await axios.get('/api/patients');
      setPatients(response.data);
    } catch (error) {
      console.error('Error fetching patients:', error);
    }
  };

  const handleSubmit = async () => {
    try {
      await axios.post('/api/patients', formData);
      fetchPatients();
      setOpen(false);
      setFormData({
        first_name: '',
        last_name: '',
        age: '',
        sex: 'male',
        bmi: '',
        children: 0,
        smoker: 'no',
        region: '',
      });
    } catch (error) {
      console.error('Error creating patient:', error);
    }
  };

  return (
    <Layout>
      <Container>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 2 }}>
          <Typography variant="h4">Patients</Typography>
          <Button
            variant="contained"
            startIcon={<AddIcon />}
            onClick={() => setOpen(true)}
          >
            Add Patient
          </Button>
        </Box>

        <TableContainer component={Paper}>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>ID</TableCell>
                <TableCell>Name</TableCell>
                <TableCell>Age</TableCell>
                <TableCell>Sex</TableCell>
                <TableCell>BMI</TableCell>
                <TableCell>Children</TableCell>
                <TableCell>Smoker</TableCell>
                <TableCell>Region</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {patients.map((patient) => (
                <TableRow key={patient.id}>
                  <TableCell>{patient.id}</TableCell>
                  <TableCell>
                    {patient.first_name} {patient.last_name}
                  </TableCell>
                  <TableCell>{patient.age}</TableCell>
                  <TableCell>{patient.sex}</TableCell>
                  <TableCell>{patient.bmi || 'N/A'}</TableCell>
                  <TableCell>{patient.children}</TableCell>
                  <TableCell>{patient.smoker}</TableCell>
                  <TableCell>{patient.region || 'N/A'}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>

        <Dialog open={open} onClose={() => setOpen(false)} maxWidth="sm" fullWidth>
          <DialogTitle>Add New Patient</DialogTitle>
          <DialogContent>
            <TextField
              fullWidth
              margin="normal"
              label="First Name"
              value={formData.first_name}
              onChange={(e) => setFormData({ ...formData, first_name: e.target.value })}
            />
            <TextField
              fullWidth
              margin="normal"
              label="Last Name"
              value={formData.last_name}
              onChange={(e) => setFormData({ ...formData, last_name: e.target.value })}
            />
            <TextField
              fullWidth
              margin="normal"
              label="Age"
              type="number"
              value={formData.age}
              onChange={(e) => setFormData({ ...formData, age: e.target.value })}
            />
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
          </DialogContent>
          <DialogActions>
            <Button onClick={() => setOpen(false)}>Cancel</Button>
            <Button onClick={handleSubmit} variant="contained">
              Add
            </Button>
          </DialogActions>
        </Dialog>
      </Container>
    </Layout>
  );
}

export default Patients;

