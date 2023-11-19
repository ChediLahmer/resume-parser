import React, { useState } from "react";
import "./App.css";
import axios from "axios";
const App = () => {
  const [file, setFile] = useState(null);
  const [MyResponse, setMyResponse] = useState("");
  const [Change, setChange] = useState(false);
  const [MyDB, setDB] = useState([]);

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    console.log(e, e.target.files[0]);
    setFile(selectedFile);
  };
  const handleSubmit = (e) => {
    e.preventDefault();

    if (!file) {
      console.error("No file selected");
      return;
    }
    const formData = new FormData();
    formData.append("pdfFile", file);
    console.log(formData);

    axios
      .post("http://localhost:5000/upload", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      })
      .then((response) => {
        console.log("File uploaded successfully:", response.data);
        setMyResponse(response.data);
      })
      .catch((error) => {
        console.error("Error uploading file:", error);
      });
  };
  const postToServer = async () => {
    try {
      const response = await axios.post(
        "http://localhost:8080/api/v1/resumes",
        MyResponse
      );
      console.log("Response from server:", response.data);
    } catch (error) {
      console.error("Error posting to server:", error);
    }
  };

  const retrieve = async () => {
    try {
      const response = await axios.get(
        "http://localhost:8080/api/v1/resumes",
        MyResponse
      );
      console.log("Response from server:", response.data);
      setDB(response.data);
    } catch (error) {
      console.error("Error posting to server:", error);
    }
  };

  const HandleChange = () => {
    setChange(!Change);
    retrieve();
  };

  return (
    <div className="App">
      <nav>
        <img className="logo" src="logo.png" alt="" />
      </nav>
      <button onClick={HandleChange}>
        {Change ? "Data Base" : "Parse Resume"}
      </button>
      {!Change && (
        <div className="main-content">
          <form onSubmit={handleSubmit} className="upload-form">
            <h2>File Upload</h2>
            <input type="file" onChange={handleFileChange} />
            {file && <p>Selected File: {file.name}</p>}
            <button type="submit">Submit</button>
            {MyResponse && (
              <div className="resume-container">
                <h3>Resume Data:</h3>
                <table className="resume-table">
                  <thead>
                    <tr>
                      <th>Key</th>
                      <th>Value</th>
                    </tr>
                  </thead>
                  <tbody>
                    {Object.entries(MyResponse).map(([key, value]) => (
                      <tr key={key}>
                        <td>{key}</td>
                        <td>
                          {Array.isArray(value) ? value.join(", ") : value}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
                <button onClick={postToServer}>Approve Data</button>
              </div>
            )}
          </form>
        </div>
      )}
      {Change && (
        <div className="main-content">
          <div className="grid-container">
            {MyDB.map((item, index) => (
              <div key={index} className="grid-item">
                <h3>Object {index + 1}</h3>
                <table className="resume-table">
                  <thead>
                    <tr>
                      <th>Key</th>
                      <th>Value</th>
                    </tr>
                  </thead>
                  <tbody>
                    {Object.entries(item).map(([key, value]) => (
                      <tr key={key}>
                        <td>{key}</td>
                        <td>
                          {Array.isArray(value) ? value.join(", ") : value}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default App;
