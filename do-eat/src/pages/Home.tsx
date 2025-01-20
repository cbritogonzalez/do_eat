import Layout from '../components/Layout';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faUtensils, faKey } from '@fortawesome/free-solid-svg-icons';
import './Home.css';

function Home() {
  return (
    <Layout>
      <div className="home-container">
        <h2 className="welcome-text">Welcome to Do Eat! 💪 </h2>
        <p><FontAwesomeIcon icon={faKey} /> You are now logged in.</p>
        <p><FontAwesomeIcon icon={faUtensils} /> Let's create your first meal plan! 
        </p>
      </div>
    </Layout>
  );
}

export default Home;