// import './css/html5reset.css';
// import './css/styles.css';
import React from 'react';

import {
  HashRouter as Router,
  Routes,
  Route
} from "react-router-dom";

import Home from './home';
import Components from './components';
import Showcase from './showcase';
import Header from './header';

const App = () => {
  return (
    <Router>
      <div>
        <Header />
        <Routes>
          <Route path="/home" element={<Home />} />
          <Route path="/contact" element={<Components />} />
          <Route path="/login" element={<Showcase />} />

          <Route exact path="/" element={<Home />} />
        </Routes>
        <p> this is a test right here</p>
      </div>
    </Router>
  );
}

export default App;