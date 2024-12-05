import './Layout.css';
import { ReactNode } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

interface LayoutProps {
  children: ReactNode;
}

function Layout({ children }: LayoutProps) {
  const navigate = useNavigate();
  const { logout } = useAuth();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <div className="layout">
      <header className="header">
        <div className="header-content">
          <h1>Do Eat</h1>
        </div>
      </header>
      <div className="main-container">
        <aside className="sidebar">
          <nav>
            <ul>
              <li onClick={() => navigate('/home')}>Home</li>
              <li onClick={() => navigate('/profile')}>Profile</li>
              <li onClick={() => navigate('/settings')}>Settings</li>
              <li onClick={handleLogout}>Logout</li>
            </ul>
          </nav>
        </aside>
        <main className="main-content">
          {children}
        </main>
      </div>
    </div>
  );
}

export default Layout; 