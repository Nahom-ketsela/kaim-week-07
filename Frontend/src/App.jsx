import React from "react";
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import DetectionsTable from "./components/DetectionsTable";
import MessagesTable from "./components/MessagesTable";

function App() {
  return (
    <Router>
      <nav>
        <Link to="/detections">Detections</Link> |
        <Link to="/messages">Telegram Messages</Link>
      </nav>
      <Routes>
        <Route path="/detections" element={<DetectionsTable />} />
        <Route path="/messages" element={<MessagesTable />} />
      </Routes>
    </Router>
  );
}

export default App;
