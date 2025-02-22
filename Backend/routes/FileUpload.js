const express = require("express");
const multer = require("multer");
const path = require("path");
const File = require("../models/Files"); // Import File model

const router = express.Router();

// Multer Storage Configuration
const storage = multer.diskStorage({
  destination: "./uploads/", // Upload folder
  filename: (req, file, cb) => {
    cb(null, file.fieldname + "-" + Date.now() + path.extname(file.originalname));
  },
});

// Multer Upload Middleware
const upload = multer({ storage });

// File Upload Route
router.post("/", upload.single("file"), async (req, res) => {
  if (!req.file) {
    return res.status(400).json({ message: "No file uploaded" });
  }

  try {
    // Save file details in MongoDB
    const newFile = new File({
      filename: req.file.filename,
      originalname: req.file.originalname,
      mimetype: req.file.mimetype,
      size: req.file.size,
    });

    await newFile.save();

    res.json({ message: "File uploaded successfully", file: req.file.filename });
  } catch (error) {
    console.error("Error saving file to DB:", error);
    res.status(500).json({ message: "Internal server error" });
  }
});

// Get All Uploaded Files Route
router.get("/", async (req, res) => {
  try {
    const files = await File.find().sort({ uploadDate: -1 });
    res.json(files);
  } catch (error) {
    console.error("Error fetching files:", error);
    res.status(500).json({ message: "Internal server error" });
  }
});

module.exports = router;
