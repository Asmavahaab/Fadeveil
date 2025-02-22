const express = require("express");
const cors = require("cors");
const mongoose = require("mongoose");
const dotenv = require("dotenv");
const path = require("path");
const fs = require("fs");

dotenv.config();
const app = express();

// Middleware
app.use(cors());
app.use(express.json()); // To parse JSON body
app.use(express.urlencoded({ extended: true })); // For form-data

// Import Routes
const loginRoute = require("./routes/login");
const registerRoute = require("./routes/register");
const uploadRoute = require("./routes/FileUpload");

// Use Routes
app.use("/api", loginRoute);
app.use("/api", registerRoute);
app.use("/api/upload", uploadRoute); // File upload route

// Serve uploaded files statically
app.use("/uploads", express.static("uploads"));

// API to fetch list of files from the 'uploads' folder
app.get("/api/files", (req, res) => {
  const UPLOADS_DIR = path.join(__dirname, "uploads");

  fs.readdir(UPLOADS_DIR, (err, files) => {
    if (err) {
      return res.status(500).send("Error reading uploads directory");
    }

    const fileDetails = files.map((file, index) => ({
      id: index + 1,
      name: file,
    }));

    res.send(fileDetails);
  });
});

// Database Connection
mongoose
  .connect(process.env.MONGO_URI)
  .then(() => console.log("✅ MongoDB Connected"))
  .catch((err) => console.error("❌ MongoDB Connection Error:", err));

// Start Server
const PORT = process.env.PORT || 5000;
app.listen(PORT, () => console.log(`✅ Server running on port ${PORT}`));
