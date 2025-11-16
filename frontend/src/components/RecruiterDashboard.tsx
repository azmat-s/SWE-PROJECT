import { Link, useNavigate } from 'react-router-dom'

interface Stat {
  label: string
  value: string
  icon: string
  color: string
}

interface Job {
  id: number
  title: string
  applications: number
  match: number
}

const RecruiterDashboard = () => {
  const navigate = useNavigate()
  
  const stats: Stat[] = [
    { label: 'Active Jobs', value: '12', icon: '💼', color: '#5B6CF1' },
    { label: 'Pending Applications', value: '48', icon: '📄', color: '#F59E0B' },
    { label: 'Shortlisted Candidates', value: '23', icon: '👥', color: '#10B981' },
    { label: 'Avg Match Score', value: '76%', icon: '📈', color: '#8B5CF6' }
  ]

  const topJobs: Job[] = [
    { id: 1, title: 'Senior Frontend Developer', applications: 18, match: 82 },
    { id: 2, title: 'Product Manager', applications: 15, match: 78 },
    { id: 3, title: 'UX Designer', applications: 12, match: 85 },
    { id: 4, title: 'Backend Engineer', applications: 10, match: 72 }
  ]

  const handleViewCandidates = (jobId: number, jobTitle: string) => {
    navigate(`/dashboard/top-candidates/${jobId}`, { 
      state: { jobTitle } 
    })
  }

  const renderStatCard = (stat: Stat, index: number) => (
    <div key={index} className="stat-card">
      <div className="stat-header">
        <span className="stat-label">{stat.label}</span>
        <div 
          className="stat-icon" 
          style={{ backgroundColor: `${stat.color}20` }}
        >
          {stat.icon}
        </div>
      </div>
      <div className="stat-value">{stat.value}</div>
    </div>
  )

  const renderJobItem = (job: Job) => (
    <div 
      key={job.id} 
      className="job-item clickable" 
      onClick={() => handleViewCandidates(job.id, job.title)}
      style={{ cursor: 'pointer' }}
    >
      <div className="job-info">
        <h3>{job.title}</h3>
        <p>{job.applications} applications</p>
      </div>
      <div className="job-match">
        <span className="match-score">{job.match}%</span>
        <span className="match-label">avg match</span>
      </div>
    </div>
  )

  return (
    <div className="dashboard-main">
      <div className="dashboard-header">
        <h1>Dashboard</h1>
        <p>Welcome back! Here's your overview</p>
      </div>

      <div className="stats-grid">
        {stats.map(renderStatCard)}
      </div>

      <div className="dashboard-grid">
        <div className="quick-actions">
          <h2>Quick Actions</h2>
          <Link to="/dashboard/view-jobs" className="action-btn primary">
            View Jobs & Review Candidates
          </Link>
          <Link to="/dashboard/post-job" className="action-btn secondary">
            Post a New Job
          </Link>
        </div>

        <div className="top-jobs">
          <h2>Top Performing Jobs</h2>
          <div className="jobs-list">
            {topJobs.map(renderJobItem)}
          </div>
        </div>
      </div>
    </div>
  )
}

export default RecruiterDashboard