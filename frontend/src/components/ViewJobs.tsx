import { Link, useNavigate } from 'react-router-dom'
import { useState } from 'react'

interface Job {
  id: number
  title: string
  applications: number
  posted: string
  status: 'active' | 'closed'
}

const ViewJobs = () => {
  const navigate = useNavigate()
  const [jobs] = useState<Job[]>([
    {
      id: 1,
      title: 'Senior Frontend Developer',
      applications: 18,
      posted: '2 days ago',
      status: 'active'
    },
    {
      id: 2,
      title: 'Product Manager',
      applications: 15,
      posted: '3 days ago',
      status: 'active'
    },
    {
      id: 3,
      title: 'UX Designer',
      applications: 12,
      posted: '5 days ago',
      status: 'active'
    },
    {
      id: 4,
      title: 'Backend Engineer',
      applications: 10,
      posted: '1 week ago',
      status: 'active'
    },
    {
      id: 5,
      title: 'Data Scientist',
      applications: 8,
      posted: '2 weeks ago',
      status: 'closed'
    }
  ])

  const handleViewCandidates = (jobId: number, jobTitle: string) => {
    navigate(`/dashboard/top-candidates/${jobId}`, { 
      state: { jobTitle } 
    })
  }

  return (
    <div className="view-jobs-container">
      <div className="page-header">
        <div>
          <h1>Posted Jobs</h1>
          <p>Manage and review your job postings</p>
        </div>
        <Link to="/dashboard/post-job" className="btn-post-job">
          + Post New Job
        </Link>
      </div>

      <div className="jobs-section">
        <h2>Active Jobs</h2>
        <div className="jobs-table">
          <table>
            <thead>
              <tr>
                <th>Job Title</th>
                <th>Applications</th>
                <th>Posted</th>
                <th>Status</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {jobs.map(job => (
                <tr key={job.id}>
                  <td className="job-title-cell">
                    <button 
                      className="job-title-link"
                      onClick={() => handleViewCandidates(job.id, job.title)}
                    >
                      {job.title}
                    </button>
                  </td>
                  <td>
                    <span className="applications-count">
                      {job.applications}
                    </span>
                  </td>
                  <td>{job.posted}</td>
                  <td>
                    <span className={`status-badge ${job.status}`}>
                      {job.status}
                    </span>
                  </td>
                  <td>
                    <button 
                      className="btn-view-candidates"
                      onClick={() => handleViewCandidates(job.id, job.title)}
                    >
                      View Candidates
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  )
}

export default ViewJobs