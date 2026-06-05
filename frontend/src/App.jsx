import { useState } from "react";
import axios from "axios";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  ResponsiveContainer,
} from "recharts";
import "./App.css";

const API_BASE_URL = "http://127.0.0.1:8000";

const exampleQuestions = [
  "Which state has the worst median AQI?",
  "Which counties had the highest Max AQI?",
  "Which counties had the most unhealthy days?",
  "Which pollutant dominated AQI days?",
  "Compare California and Texas",
];

function App() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [intent, setIntent] = useState("");
  const [data, setData] = useState([]);
  const [chart, setChart] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const askQuestion = async (customQuestion = null) => {
    const finalQuestion = customQuestion || question;

    if (!finalQuestion.trim()) {
      setError("Please enter a question.");
      return;
    }

    try {
      setLoading(true);
      setError("");
      setAnswer("");
      setIntent("");
      setData([]);
      setChart(null);

      const response = await axios.post(`${API_BASE_URL}/api/chat/ask`, {
        question: finalQuestion,
      });

      setAnswer(response.data.answer);
      setIntent(response.data.intent);
      setData(response.data.data || []);
      setChart(response.data.chart || null);

      if (customQuestion) {
        setQuestion(customQuestion);
      }
    } catch (err) {
      console.error(err);
      setError("Something went wrong. Make sure your backend is running on port 8000.");
    } finally {
      setLoading(false);
    }
  };

  const renderChart = () => {
    if (!chart || !data || data.length === 0) return null;

    return (
      <section className="card">
        <h2>{chart.title}</h2>

        <ResponsiveContainer width="100%" height={350}>
          <BarChart data={data}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis
              dataKey={chart.x_key}
              angle={-25}
              textAnchor="end"
              height={90}
            />
            <YAxis />
            <Tooltip />
            <Bar dataKey={chart.y_key} />
          </BarChart>
        </ResponsiveContainer>
      </section>
    );
  };

  const renderTable = () => {
    if (!data || data.length === 0) return null;

    const columns = Object.keys(data[0]);

    return (
      <section className="card">
        <h2>Calculated Data</h2>

        <div className="table-wrapper">
          <table>
            <thead>
              <tr>
                {columns.map((col) => (
                  <th key={col}>{col}</th>
                ))}
              </tr>
            </thead>

            <tbody>
              {data.map((row, index) => (
                <tr key={index}>
                  {columns.map((col) => (
                    <td key={col}>{row[col]}</td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>
    );
  };

  return (
    <main className="page">
      <header className="hero">
        <p className="badge">Government Dataset + FastAPI + Gemini</p>
        <h1>GovData AI Analyst</h1>
        <p>
          Ask questions about the EPA 2024 Annual AQI by County dataset and get
          verified analytics, AI explanations, tables, and charts.
        </p>
      </header>

      <section className="card">
        <label className="label">Ask a question</label>

        <div className="input-row">
          <input
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            placeholder="Example: Which state has the worst median AQI?"
            onKeyDown={(e) => {
              if (e.key === "Enter") askQuestion();
            }}
          />

          <button onClick={() => askQuestion()} disabled={loading}>
            {loading ? "Analyzing..." : "Ask"}
          </button>
        </div>

        <div className="examples">
          {exampleQuestions.map((q) => (
            <button key={q} onClick={() => askQuestion(q)}>
              {q}
            </button>
          ))}
        </div>

        {error && <p className="error">{error}</p>}
      </section>

      {answer && (
        <section className="card">
          <p className="intent">Detected intent: {intent}</p>
          <h2>AI Explanation</h2>
          <p className="answer">{answer}</p>
        </section>
      )}

      {renderChart()}
      {renderTable()}
    </main>
  );
}

export default App;