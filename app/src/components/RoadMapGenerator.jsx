import React from "react"
import { useState } from "react"
import axios from "axios"
import "./RoadmapGenerator.css"

function RoadmapGenerator() {
  const [formData, setFormData] = useState({
    skill: "",
    experience: "",
    time_duration: "",
    purpose: "",
  })
  const [roadmap, setRoadmap] = useState("")
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState("")

  const handleInputChange = (e) => {
    const { name, value } = e.target
    setFormData((prevData) => ({
      ...prevData,
      [name]: value,
    }))
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError("")
    setRoadmap("")

    try {
      const response = await axios.post("https://test-wjqk.onrender.com/generate-roadmap", formData)
      setRoadmap(response.data.roadmap)
    } catch (err) {
      setError("An error occurred while generating the roadmap. Please try again.")
      console.error("Error:", err)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="roadmap-generator">
      <h1>Roadmap Generator</h1>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="skill">Skill</label>
          <input
            type="text"
            id="skill"
            name="skill"
            value={formData.skill}
            onChange={handleInputChange}
            required
            placeholder="e.g. React, Machine Learning, Data Science"
          />
        </div>
        <div className="form-group">
          <label htmlFor="experience">Experience Level</label>
          <input
            type="text"
            id="experience"
            name="experience"
            value={formData.experience}
            onChange={handleInputChange}
            required
            placeholder="e.g. Beginner, Intermediate, Advanced"
          />
        </div>
        <div className="form-group">
          <label htmlFor="time_duration">Time Duration</label>
          <input
            type="text"
            id="time_duration"
            name="time_duration"
            value={formData.time_duration}
            onChange={handleInputChange}
            required
            placeholder="e.g. 3 months, 6 weeks, 1 year"
          />
        </div>
        <div className="form-group">
          <label htmlFor="purpose">Learning Purpose</label>
          <textarea
            id="purpose"
            name="purpose"
            value={formData.purpose}
            onChange={handleInputChange}
            required
            placeholder="e.g. Career change, Skill improvement, Personal project"
          />
        </div>
        <button type="submit" disabled={loading}>
          {loading ? "Generating..." : "Generate Roadmap"}
        </button>
      </form>

      {error && <p className="error">{error}</p>}

      {roadmap && (
        <div className="roadmap">
          <h2>Your Learning Roadmap</h2>
          <pre>{roadmap}</pre>
        </div>
      )}
    </div>
  )
}

export default RoadmapGenerator
