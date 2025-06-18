const express = require("express");
const path = require("path");
const axios = require("axios");

const app = express();
const PORT = 3000;
const FASTAPI_URL = "http://0.0.0.0:8000/query";  // ✅ Ensure correct FastAPI endpoint

app.use(express.json());
app.use(express.static("public"));  // ✅ Serve frontend files (index.html)

// ✅ Serve the frontend when users visit the homepage
app.get("/", (req, res) => {
    res.sendFile(path.join(__dirname, "public/index.html"));
});

// ✅ Handle chatbot queries
app.post("/query", async (req, res) => {
    const userQuery = req.body.query;
    try {
        const response = await axios.get(`${FASTAPI_URL}?user_query=${encodeURIComponent(userQuery)}`);
        res.json(response.data);
    } catch (error) {
        console.error("Error:", error);
        res.status(500).json({ error: "FastAPI request failed" });
    }
});

app.listen(PORT, () => {
    console.log(`Node.js server running on http://localhost:${PORT}`);
});
