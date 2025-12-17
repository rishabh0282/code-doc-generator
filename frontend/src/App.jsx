import React from "react";
import Parser from "./components/Parser";
import "./App.css";

export default function App() {
  return (
    <div className="app-container">
      <header className="app-header">
        <h1>?? Code Doc Generator</h1>
        <p>Parse code and generate documentation with AI</p>
      </header>
      <main className="app-main">
        <Parser />
      </main>
      <footer className="app-footer">
        <p>Powered by LangChain + OpenAI + FastAPI</p>
      </footer>
    </div>
  );
}
