import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './context/AuthProvider';
import { ThemeProvider, createTheme, CssBaseline } from '@mui/material';
import Login from './pages/Login';
import Home from './pages/Home';
import Profile from './pages/Profile';
import Settings from './pages/Settings';
import Setup from './pages/SetUp'; // Import the new Setup component
import MealPlan from './pages/MealPlan'; // Import the new MealPlan component
import './App.css';

// Create a theme instance
const theme = createTheme({
  palette: {
    primary: {
      main: '#1976d2',
    },
    secondary: {
      main: '#dc004e',
    },
  },
});

// Protected Route wrapper component
function ProtectedRoute({ children }: { children: React.JSX.Element }) {
  const isAuthenticated = localStorage.getItem('isAuthenticated') === 'true';
  
  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  return children;
}

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline /> {/* Provides a consistent baseline styles */}
      <AuthProvider>
        <Router>
          <Routes>
            <Route path="/" element={<Navigate to="/login" replace />} />
            <Route path="/login" element={<Login />} />
            <Route
              path="/home"
              element={
                <ProtectedRoute>
                  <Home />
                </ProtectedRoute>
              }
            />
            <Route
              path="/profile"
              element={
                <ProtectedRoute>
                  <Profile />
                </ProtectedRoute>
              }
            />
            <Route
              path="/settings"
              element={
                <ProtectedRoute>
                  <Settings />
                </ProtectedRoute>
              }
            />
            <Route
              path="/setup"
              element={
                <ProtectedRoute>
                  <Setup />
                </ProtectedRoute>
              }
            />
            <Route
              path="/mealplan"
              element={
                <ProtectedRoute>
                  <MealPlan />
                </ProtectedRoute>
              }
            />
          </Routes>
        </Router>
      </AuthProvider>
    </ThemeProvider>
  );
}

export default App;
