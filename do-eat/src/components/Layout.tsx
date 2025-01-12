import { ReactNode } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/useAuth';
import {
  AppBar,
  Toolbar,
  Typography,
  Button,
  Drawer,
  List,
  ListItemIcon,
  ListItemText,
  Box,
  Container,
  ListItemButton,
} from '@mui/material';
import './Layout.css';
import HomeIcon from '@mui/icons-material/Home';
import ProfileIcon from '@mui/icons-material/Person';
import SettingsIcon from '@mui/icons-material/Settings';
import MealPlanIcon from '@mui/icons-material/RestaurantMenu';
import { Logout as LogoutIcon } from '@mui/icons-material';

interface LayoutProps {
  children: ReactNode;
}

const getCookie = (name) => {
  const cookieString = document.cookie;
  const cookies = cookieString.split("; ");
  for (let cookie of cookies) {
      const [key, value] = cookie.split("=");
      if (key === name) return decodeURIComponent(value);
  }
  return null; // Return null if the cookie is not found
};


function Layout({ children }: LayoutProps) {
  const navigate = useNavigate();
  const { logout } = useAuth();

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  const drawerWidth = 240;

  return (
    <Box sx={{ display: 'flex' }}>
      <AppBar position="fixed" sx={{ zIndex: (theme) => theme.zIndex.drawer + 1, backgroundColor: '#355c66' }}>
        <Toolbar>
          <img src="../public/do_eat_logo.png" alt="Do Eat Logo" className="header-logo" />
          <Button
            color="inherit"
            onClick={handleLogout}
            startIcon={<LogoutIcon />}
            sx={{ marginLeft: 'auto', padding: '0.5rem 1rem', width: '150px' }}
          >
            Logout
          </Button>
        </Toolbar>
      </AppBar>

      <Drawer
        variant="permanent"
        sx={{
          width: drawerWidth,
          flexShrink: 0,
          [`& .MuiDrawer-paper`]: { width: drawerWidth, boxSizing: 'border-box' },
        }}
      >
        <Toolbar /> {/* This creates space for the AppBar */}
        <Box sx={{ overflow: 'auto' }}>
          <List>
            <ListItemButton onClick={() => navigate('/home')}>
              <ListItemIcon><HomeIcon sx={{ color: '#355c66' }} /></ListItemIcon>
              <ListItemText primary="Home" />
            </ListItemButton>
            <ListItemButton onClick={() => navigate('/profile')}>
              <ListItemIcon><ProfileIcon sx={{ color: '#355c66' }} /></ListItemIcon>
              <ListItemText primary="Profile" />
            </ListItemButton>
            <ListItemButton onClick={() => navigate('/settings')}>
              <ListItemIcon><SettingsIcon sx={{ color: '#355c66' }} /></ListItemIcon>
              <ListItemText primary="Settings" />
            </ListItemButton>
            <ListItemButton onClick={() => navigate('/mealplan')}>
              <ListItemIcon><MealPlanIcon sx={{ color: '#355c66' }} /></ListItemIcon>
              <ListItemText primary="Meal Plan" />
            </ListItemButton>
            <ListItemButton onClick={() => {
              const email = getCookie("email")?.replace(/"/g, "");
              fetch('http://localhost:3000/createMeals?email=' + email, { method: 'POST' })
              .then(response => response.json())
              .then(data => console.log(data))
              .catch(error => console.error('Error:', error));
            }}>
              <ListItemIcon><SettingsIcon /></ListItemIcon>
              <ListItemText primary="Generate recipes" />
            </ListItemButton>
          </List>
        </Box>
      </Drawer>

      <Box component="main" sx={{ flexGrow: 1, p: 3 }}>
        <Toolbar /> {/* This creates space for the AppBar */}
        <Container>
          {children}
        </Container>
      </Box>
    </Box>
  );
}

export default Layout;