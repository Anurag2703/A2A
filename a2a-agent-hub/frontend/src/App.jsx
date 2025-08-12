// import { useState } from "react";
// import axios from "axios";
// import "./App.css"; // vanilla CSS

// function App() {
//   const [prompt, setPrompt] = useState("");
//   const [file, setFile] = useState(null);
//   const [result, setResult] = useState(null);
//   const [loading, setLoading] = useState(false);
//   const [error, setError] = useState("");

//   const handleSubmit = async () => {
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
//         {
//           headers: { "Content-Type": "multipart/form-data" },
//         }
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

//   const RenderObject = ({ data }) => {
//     if (typeof data !== "object" || data === null) {
//       return <span>{String(data)}</span>;
//     }
//     if (Array.isArray(data)) {
//       return (
//         <ul style={{ paddingLeft: "1.2rem" }}>
//           {data.map((item, idx) => (
//             <li key={idx}>
//               <RenderObject data={item} />
//             </li>
//           ))}
//         </ul>
//       );
//     }
//     return (
//       <div
//         style={{
//           paddingLeft: "1rem",
//           borderLeft: "2px solid #ddd",
//           marginBottom: "0.5rem",
//         }}
//       >
//         {Object.entries(data).map(([key, value]) => (
//           <div key={key} style={{ marginBottom: "0.3rem" }}>
//             <strong>{key}:</strong>{" "}
//             {typeof value === "object" && value !== null ? (
//               <RenderObject data={value} />
//             ) : (
//               <span>{String(value)}</span>
//             )}
//           </div>
//         ))}
//       </div>
//     );
//   };

//   return (
//     <div className="page-root">
//       {/* Main content area */}
//       <div className="main-wrap">
//         <div className="container">
//           {/* Header */}
//           <div className="header">
//             <div className="logo" aria-hidden="true">
//               <div className="logo-shape" />
//             </div>

//             <div className="header-text">
//               <p className="subtitle">Welcome to Legal Document Summarizer</p>
//               <h1 className="title">How can I help?</h1>
//             </div>
//           </div>

//           {/* File upload + prompt fields */}
//           <div className="card">
//             <label className="label">Prompt:</label>
//             <textarea
//               value={prompt}
//               onChange={(e) => setPrompt(e.target.value)}
//               rows="3"
//               className="textarea"
//             />

//             <label className="label">Upload File:</label>
//             <input
//               type="file"
//               onChange={(e) => setFile(e.target.files[0])}
//               accept=".pdf,.doc,.docx,.txt"
//               className="file-input"
//             />
//             {file && (
//               <p className="selected-file">
//                 Selected file: <strong>{file.name}</strong>
//               </p>
//             )}

//             {error && <p className="error-text">{error}</p>}
//             {loading && <p className="loading-text">Processing...</p>}

//             {result && (
//               <div className="result-wrap">
//                 <h2 className="result-title">Result</h2>
//                 <div className="result-box">
//                   <RenderObject data={result} />
//                 </div>
//               </div>
//             )}
//           </div>
//         </div>
//       </div>

//       {/* Bottom section with plain input + button */}
//       <div className="bottom-sticky">
//         <div className="bottom-inner">
//           <input
//             type="text"
//             className="chat-input"
//             value={prompt}
//             onChange={(e) => setPrompt(e.target.value)}
//             placeholder="Enter your prompt and submit..."
//           />
//           <button className="chat-button" onClick={handleSubmit}>
//             Send
//           </button>
//         </div>
//       </div>
//     </div>
//   );
// }

// export default App;







import { useState } from "react";
import axios from "axios";

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
      // Build FormData to match FastAPI's Form(...) + File(...)
      const formData = new FormData();
      formData.append("prompt", prompt.trim());
      formData.append("file", file);

      console.log("Sending FormData to API");

      const res = await axios.post(
        "http://localhost:8000/agents/summarizer_agent/run",
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
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

  // Helper component to render object nicely
  const RenderObject = ({ data }) => {
    if (typeof data !== "object" || data === null) {
      return <span>{String(data)}</span>;
    }
    if (Array.isArray(data)) {
      return (
        <ul style={{ paddingLeft: "1.2rem" }}>
          {data.map((item, idx) => (
            <li key={idx}>
              <RenderObject data={item} />
            </li>
          ))}
        </ul>
      );
    }
    // For plain objects
    return (
      <div style={{ paddingLeft: "1rem", borderLeft: "2px solid #ddd", marginBottom: "0.5rem" }}>
        {Object.entries(data).map(([key, value]) => (
          <div key={key} style={{ marginBottom: "0.3rem" }}>
            <strong>{key}:</strong>{" "}
            {typeof value === "object" && value !== null ? (
              <RenderObject data={value} />
            ) : (
              <span>{String(value)}</span>
            )}
          </div>
        ))}
      </div>
    );
  };

  return (
    <div style={{ maxWidth: "600px", margin: "auto", padding: "1rem" }}>
      <h1>Legal Document Summarizer</h1>
      <form onSubmit={handleSubmit}>
        <div style={{ marginBottom: "1rem" }}>
          <label>Prompt:</label>
          <textarea
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            rows="3"
            style={{ width: "100%" }}
          />
        </div>
        <div style={{ marginBottom: "1rem" }}>
          <label>Upload File:</label>
          <input
            type="file"
            onChange={(e) => setFile(e.target.files[0])}
            accept=".pdf,.doc,.docx,.txt"
          />
          {file && (
            <p style={{ fontStyle: "italic", marginTop: "0.3rem" }}>
              Selected file: <strong>{file.name}</strong>
            </p>
          )}
        </div>
        <button type="submit" disabled={loading}>
          {loading ? "Processing..." : "Submit"}
        </button>
      </form>

      {error && <p style={{ color: "red" }}>{error}</p>}

      {result && (
        <div style={{ marginTop: "1rem" }}>
          <h2>Result</h2>
          <div
            style={{
              background: "#000000ff",
              padding: "1rem",
              borderRadius: "5px",
              color: "white",
              fontFamily: "monospace",
              whiteSpace: "pre-wrap",
              wordWrap: "break-word",
            }}
          >
            <RenderObject data={result} />
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
