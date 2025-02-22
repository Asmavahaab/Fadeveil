const mongoose = require("mongoose");

// User Schema
const UserSchema = new mongoose.Schema({
  name: {
    type: String,
    required: true,
    trim: true,
  },
  email: {
    type: String,
    required: true,
    unique: true,
    trim: true,
    lowercase: true,
  },
  password: {
    type: String,
    required: true,
    minlength: 4, // Keeping it 4 as per provided data, but recommend using at least 6-8 chars for security
  },
  role: {
    type: String,
    required: true,
    enum: ["Cyber Researcher", "Incident Responder"], // Ensures only valid roles are stored
  },
  createdAt: {
    type: Date,
    default: Date.now, // Automatically adds a timestamp when a user is created
  },
});

// Export User Model
module.exports = mongoose.model("User", UserSchema);
