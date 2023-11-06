import React, { useState } from "react";
import axios from "axios";

function App() {
  const [input, setInput] = useState("");
  const [response, setResponse] = useState("");

  const handleSubmit = async () => {
    try {
      const res = await axios.post("http://localhost:5000/command", { input });
      setResponse(res.data.output);
    } catch (error) {
      console.error("There was an error sending the request", error);
    }
  };

  return (
    <div className="App">
      <h1>Sebastian</h1>
      <input
        type="text"
        value={input}
        onChange={(e) => setInput(e.target.value)}
      />
      <button onClick={handleSubmit}>Submit</button>
      <p>Sebastian says: {response}</p>
    </div>
  );
}

export default App;
