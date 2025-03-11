import React, { useState } from "react";
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import DetectionsTable from "./components/DetectionsTable";
import MessagesTable from "./components/MessagesTable";

function App() {
  const [activeTab, setActiveTab] = useState("/detections");

  return (
    <Router>
      <nav>
        <h1>Frontend Dashboard</h1>
        <Link
          to="/detections"
          className={activeTab === "/detections" ? "active" : ""}
          onClick={() => setActiveTab("/detections")}
        >
          Detections
        </Link>
        |
        <Link
          to="/messages"
          className={activeTab === "/messages" ? "active" : ""}
          onClick={() => setActiveTab("/messages")}
        >
          Telegram Messages
        </Link>
      </nav>
      <main>
        <Routes>
          <Route path="/detections" element={<DetectionsTable />} />
          <Route path="/messages" element={<MessagesTable />} />
        </Routes>
      </main>
    </Router>
  );
}

export default App;
