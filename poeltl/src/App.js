import React, { useState } from 'react';

function App() {
  const [name, setName] = useState("");
  const [age, setAge] = useState(0);
  const [modifiedName, setModifiedName] = useState("");
  const [modifiedAge, setModifiedAge] = useState(null);

  const handleSubmit = (event) => {
    event.preventDefault();

    fetch("/get-members" ,{

      method:"POST",
      headers:{
        "Content-Type": "application/json"
      },
      body: JSON.stringify({name , age})

    })
    .then(
      response => response.json()
    )
    .then(data => {
      setModifiedName(data.name)
      setModifiedAge(data.age)
    })
    .catch(error => console.error("Error:", error));

  };
  return (
    <div>
      <h1>Enter Name and Age</h1>
      <form onSubmit={handleSubmit}>
        <div>
          <label>Name: </label>
          <input
            type="text"
            value={name}
            onChange={(e) => setName(e.target.value)}
            placeholder="Enter your name"
          />
        </div>
        <div>
          <label>Age: </label>
          <input
            type="number"
            value={age}
            onChange={(e) => setAge(e.target.value)}
            placeholder="Enter your age"
          />
        </div>
        <button type="submit">Submit</button>
      </form>

      {modifiedName && modifiedAge && (
        <div>
          <h2>Modified Data from Backend:</h2>
          <p><strong>Name:</strong> {modifiedName}</p>
          <p><strong>Age:</strong> {modifiedAge}</p>
        </div>
      )}
    </div>
  );
}

export default App;
