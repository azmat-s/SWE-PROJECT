import { useParams, useNavigate, useLocation } from 'react-router-dom'
import { useState, useEffect } from 'react'
import '../styles/top-candidates.css'

interface Candidate {
  id: number
  name: string
  role: string
  experience: string
  matchScore: number
  skills: string[]
  status: 'Shortlisted' | 'Reviewing' | 'New'
}

interface LocationState {
  jobTitle?: string
}

const TopCandidates = () => {
  const { jobId } = useParams<{ jobId: string }>()
  const navigate = useNavigate()
  const location = useLocation()
  const [candidates, setCandidates] = useState<Candidate[]>([])
  const [jobTitle, setJobTitle] = useState<string>('')

  useEffect(() => {
    initializeComponent()
  }, [location.state])

  const initializeComponent = () => {
    const state = location.state as LocationState
    setJobTitle(state?.jobTitle || 'Senior Frontend Developer')
    loadCandidatesData()
  }

  const loadCandidatesData = () => {
    const mockCandidates: Candidate[] = [
      {
        id: 1,
        name: 'Sarah Johnson',
        role: 'Senior Frontend Developer',
        experience: '7 years',
        matchScore: 95,
        skills: ['React', 'TypeScript', 'Node.js'],
        status: 'Shortlisted'
      },
      {
        id: 2,
        name: 'Michael Chen',
        role: 'Full Stack Developer',
        experience: '5 years',
        matchScore: 88,
        skills: ['React', 'Python', 'AWS'],
        status: 'Reviewing'
      },
      {
        id: 3,
        name: 'Emily Rodriguez',
        role: 'Frontend Developer',
        experience: '4 years',
        matchScore: 82,
        skills: ['Vue.js', 'JavaScript', 'CSS'],
        status: 'New'
      }
    ]
    setCandidates(mockCandidates)
  }

  const getInitials = (name: string): string => {
    return name
      .split(' ')
      .map(word => word[0])
      .join('')
      .toUpperCase()
  }

  const handleBackNavigation = () => {
    navigate('/dashboard/view-jobs')
  }

  const handleViewProfile = (candidateId: number) => {
    console.log('View profile for candidate:', candidateId)
  }

  const handleSendMessage = (candidateId: number) => {
    navigate('/dashboard/messages')
  }

  const getStatusClass = (status: string): string => {
    return status.toLowerCase()
  }

  return (
    <div className="dashboard-main">
      <div className="dashboard-header">
        <div>
          <h1>Top Candidates</h1>
          <p>Review candidates for {jobTitle}</p>
        </div>
        <button 
          onClick={handleBackNavigation} 
          className="action-btn primary"
        >
          ← Back to Jobs
        </button>
      </div>

      <div className="candidates-container">
        {candidates.map(candidate => (
          <div key={candidate.id} className="candidate-card">
            <div className="candidate-header">
              <div className="candidate-avatar">
                {getInitials(candidate.name)}
              </div>
              <div className="candidate-info">
                <h3>{candidate.name}</h3>
                <p>{candidate.role}</p>
                <span className="experience">{candidate.experience}</span>
              </div>
              <div className="match-score-container">
                <span className="match-score">{candidate.matchScore}%</span>
                <span className="match-label">Match</span>
              </div>
            </div>
            
            <div className="candidate-skills">
              {candidate.skills.map((skill, index) => (
                <span key={index} className="skill-tag">
                  {skill}
                </span>
              ))}
            </div>
            
            <div className="candidate-actions">
              <button 
                className="action-btn primary"
                onClick={() => handleViewProfile(candidate.id)}
              >
                View Profile
              </button>
              <button 
                className="action-btn secondary"
                onClick={() => handleSendMessage(candidate.id)}
              >
                Message
              </button>
              <span className={`status-badge ${getStatusClass(candidate.status)}`}>
                {candidate.status}
              </span>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

export default TopCandidates