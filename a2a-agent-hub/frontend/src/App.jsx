import { useState } from "react";
import axios from "axios";
import "./App.css";
import UniversalRenderer from "./components/UniversalRenderer";
import jsPDF from "jspdf";
import autoTable from "jspdf-autotable";

function App() {
  const [prompt, setPrompt] = useState("");
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!prompt.trim()) {
      setError("Prompt is required");
      return;
    }
    if (!file) {
      setError("Please upload a file");
      return;
    }

    setError("");
    setLoading(true);
    setResult(null);

    try {
      const formData = new FormData();
      formData.append("prompt", prompt.trim());
      formData.append("file", file);

      const res = await axios.post(
        "http://localhost:8000/agents/summarizer_agent/run",
        formData,
        { headers: { "Content-Type": "multipart/form-data" } }
      );

      setResult(res.data);
    } catch (err) {
      console.error("API error:", err.response?.data || err.message);
      setError(
        err.response?.data?.detail?.[0]?.msg || "An error occurred. Try again."
      );
    } finally {
      setLoading(false);
    }
  };

  const handleDownloadPDF = () => {
    const doc = new jsPDF();

    // Flatten the result into rows for the PDF
    const rows = [];
    const buildRows = (data, parentKey = "") => {
      if (typeof data !== "object" || data === null) {
        rows.push([parentKey || "Value", String(data)]);
        return;
      }
      if (Array.isArray(data)) {
        data.forEach((item, idx) =>
          buildRows(item, `${parentKey}[${idx}]`)
        );
        return;
      }
      Object.entries(data).forEach(([key, value]) => {
        const fullKey = parentKey ? `${parentKey} → ${key}` : key;
        if (typeof value === "object" && value !== null) {
          buildRows(value, fullKey);
        } else {
          rows.push([fullKey, String(value)]);
        }
      });
    };

    buildRows(result);

    autoTable(doc, {
      head: [["Field", "Value"]],
      body: rows,
      styles: {
        fontSize: 11,
        cellPadding: 4,
        lineColor: [200, 200, 200],
        lineWidth: 0.2,
        textColor: [33, 37, 41], // dark gray text
        halign: "left",
        valign: "middle"
      },
      headStyles: {
        fillColor: [240, 240, 240], // light gray background like your header
        textColor: [0, 0, 0],
        fontStyle: "bold",
        halign: "left",
        lineWidth: 0.3,
        lineColor: [180, 180, 180]
      },
      alternateRowStyles: {
        fillColor: [250, 250, 250] // subtle zebra stripes
      },
      columnStyles: {
        0: { cellWidth: 70 },
        1: { cellWidth: "auto" }
      }
    });

    doc.save("summary.pdf");
  };

  return (
    <div className="app-container">
      <h1>Legal Document Summarizer</h1>
      <form onSubmit={handleSubmit} className="form-container">
        <div className="form-group">
          <label><strong>PROMPT:</strong></label>
          <textarea
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            rows="3"
            className="textarea"
          />
        </div>
        <div className="form-group">
          <label>Upload File: </label>
          <input
            type="file"
            onChange={(e) => setFile(e.target.files[0])}
            accept=".pdf,.doc,.docx,.txt"
            className="file-input"
          />
          {file && <p className="file-name">Selected file: {file.name}</p>}
        </div>
        <button type="submit" disabled={loading} className="submit-btn">
          {loading ? "Processing..." : "Submit"}
        </button>
      </form>

      {error && <p className="error">{error}</p>}

      {result && (
        <div className="result-container">
          <h2>Result</h2>
          <div className="result-box">
            <UniversalRenderer data={result} />
          </div>
          <button
            onClick={handleDownloadPDF}
            className="download-btn"
            style={{
              marginTop: "1rem",
              padding: "0.5rem 1rem",
              background: "#28a745",
              color: "#fff",
              border: "none",
              borderRadius: "5px",
              cursor: "pointer"
            }}
          >
            Download as PDF
          </button>
        </div>
      )}
    </div>
  );
}

export default App;




// import { useState } from "react";
// import axios from "axios";
// import "./App.css";
// import UniversalRenderer from "./components/UniversalRenderer"; // NEW

// function App() {
//   const [prompt, setPrompt] = useState("");
//   const [file, setFile] = useState(null);
//   const [result, setResult] = useState(null);
//   const [loading, setLoading] = useState(false);
//   const [error, setError] = useState("");

//   const handleSubmit = async (e) => {
//     e.preventDefault();

//     if (!prompt.trim()) {
//       setError("Prompt is required");
//       return;
//     }
//     if (!file) {
//       setError("Please upload a file");
//       return;
//     }

//     setError("");
//     setLoading(true);
//     setResult(null);

//     try {
//       const formData = new FormData();
//       formData.append("prompt", prompt.trim());
//       formData.append("file", file);

//       const res = await axios.post(
//         "http://localhost:8000/agents/summarizer_agent/run",
//         formData,
//         { headers: { "Content-Type": "multipart/form-data" } }
//       );

//       setResult(res.data);
//     } catch (err) {
//       console.error("API error:", err.response?.data || err.message);
//       setError(
//         err.response?.data?.detail?.[0]?.msg || "An error occurred. Try again."
//       );
//     } finally {
//       setLoading(false);
//     }
//   };

//   return (
//     <div className="app-container">
//       <h1>Legal Document Summarizer</h1>
//       <form onSubmit={handleSubmit} className="form-container">
//         <div className="form-group">
//           <label><strong>PROMPT:</strong></label>
//           <textarea
//             value={prompt}
//             onChange={(e) => setPrompt(e.target.value)}
//             rows="3"
//             className="textarea"
//           />
//         </div>
//         <div className="form-group">
//           <label>Upload File: </label>
//           <input
//             type="file"
//             onChange={(e) => setFile(e.target.files[0])}
//             accept=".pdf,.doc,.docx,.txt"
//             className="file-input"
//           />
//           {file && <p className="file-name">Selected file: {file.name}</p>}
//         </div>
//         <button type="submit" disabled={loading} className="submit-btn">
//           {loading ? "Processing..." : "Submit"}
//         </button>
//       </form>

//       {error && <p className="error">{error}</p>}

//       {result && (
//         <div className="result-container">
//           <h2>Result</h2>
//           <div className="result-box">
//             <UniversalRenderer data={result} />
//           </div>
//         </div>
//       )}
//     </div>
//   );
// }

// export default App;