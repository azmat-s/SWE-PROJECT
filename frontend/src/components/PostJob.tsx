// components/dashboard/PostJob.tsx
import { useState } from 'react'

const PostJob = () => {
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    skills: '',
    experience: '',
    location: '',
    minSalary: '',
    maxSalary: ''
  })

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    console.log('Job posted:', formData)
  }

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    })
  }

  return (
    <div className="post-job-container">
      <div className="page-header">
        <h1>Post a New Job</h1>
        <p>Create a job listing to find your ideal candidate</p>
      </div>

      <div className="job-form-section">
        <h2>Job Details</h2>
        
        <form onSubmit={handleSubmit} className="job-form">
          <div className="form-group">
            <label htmlFor="title">Job Title</label>
            <input
              type="text"
              id="title"
              name="title"
              placeholder="e.g. Senior Frontend Developer"
              value={formData.title}
              onChange={handleChange}
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="description">
              Job Description
              <span className="ai-assist">🤖 AI Assist</span>
            </label>
            <textarea
              id="description"
              name="description"
              placeholder="Describe the role, responsibilities, and requirements..."
              rows={6}
              value={formData.description}
              onChange={handleChange}
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="skills">Required Skills (comma-separated)</label>
            <input
              type="text"
              id="skills"
              name="skills"
              placeholder="React, TypeScript, Node.js, AWS"
              value={formData.skills}
              onChange={handleChange}
              required
            />
          </div>

          <div className="form-row">
            <div className="form-group">
              <label htmlFor="experience">Experience Level</label>
              <select
                id="experience"
                name="experience"
                value={formData.experience}
                onChange={handleChange}
                required
              >
                <option value="">Select level</option>
                <option value="entry">Entry Level</option>
                <option value="mid">Mid Level</option>
                <option value="senior">Senior Level</option>
                <option value="lead">Lead/Principal</option>
              </select>
            </div>

            <div className="form-group">
              <label htmlFor="location">Location</label>
              <input
                type="text"
                id="location"
                name="location"
                placeholder="e.g. San Francisco, CA or Remote"
                value={formData.location}
                onChange={handleChange}
                required
              />
            </div>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label htmlFor="minSalary">Min Salary ($)</label>
              <input
                type="number"
                id="minSalary"
                name="minSalary"
                placeholder="80000"
                value={formData.minSalary}
                onChange={handleChange}
              />
            </div>

            <div className="form-group">
              <label htmlFor="maxSalary">Max Salary ($)</label>
              <input
                type="number"
                id="maxSalary"
                name="maxSalary"
                placeholder="120000"
                value={formData.maxSalary}
                onChange={handleChange}
              />
            </div>
          </div>

          <div className="form-actions">
            <button type="submit" className="btn-submit">Submit Job</button>
            <button type="button" className="btn-cancel">Cancel</button>
          </div>
        </form>
      </div>
    </div>
  )
}

export default PostJob