import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import styles from '../styles/jobseeker.module.css'

interface JobStats {
  totalApplications: number
  matchScore: number
  pendingApplications: number
  profileStrength: number
}

interface RecentApplication {
  id: string
  jobTitle: string
  company: string
  matchScore: number
  status: 'shortlisted' | 'pending' | 'rejected'
  appliedDate: string
}

const JobSeekerDashboard = () => {
  const navigate = useNavigate()
  const [stats, setStats] = useState<JobStats>({
    totalApplications: 8,
    matchScore: 82,
    pendingApplications: 5,
    profileStrength: 85
  })

  const [recentApplications] = useState<RecentApplication[]>([
    {
      id: '1',
      jobTitle: 'Senior Frontend Developer',
      company: 'TechCorp',
      matchScore: 92,
      status: 'shortlisted',
      appliedDate: '2025-11-07'
    },
    {
      id: '2',
      jobTitle: 'React Developer',
      company: 'StartupXYZ',
      matchScore: 87,
      status: 'pending',
      appliedDate: '2025-11-06'
    },
    {
      id: '3',
      jobTitle: 'Full Stack Engineer',
      company: 'Digital Solutions',
      matchScore: 84,
      status: 'pending',
      appliedDate: '2025-11-04'
    }
  ])

  const handleSearchJobs = () => {
    navigate('/dashboard/search-jobs')
  }

  const handleViewApplications = () => {
    navigate('/dashboard/my-applications')
  }

  const handleUpdateProfile = () => {
    navigate('/dashboard/profile')
  }

  return (
    <div className={styles.dashboardContainer}>
      <div className={styles.dashboardHeader}>
        <div>
          <h1>Dashboard</h1>
          <p>Welcome back! Here's your job search overview</p>
        </div>
      </div>

      <div className={styles.statsGrid}>
        <div className={styles.statCard}>
          <div className={styles.statHeader}>
            <span className={styles.statLabel}>Total Applications</span>
            <div className={`${styles.statIcon} ${styles.iconApplications}`}>
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                <path d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
              </svg>
            </div>
          </div>
          <div className={styles.statValue}>{stats.totalApplications}</div>
        </div>

        <div className={styles.statCard}>
          <div className={styles.statHeader}>
            <span className={styles.statLabel}>Average Match Score</span>
            <div className={`${styles.statIcon} ${styles.iconMatch}`}>
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                <path d="M9 19V6l12-3v13M9 19c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2zm12-3c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2zM9 10l12-3" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
              </svg>
            </div>
          </div>
          <div className={styles.statValue}>{stats.matchScore}%</div>
        </div>

        <div className={styles.statCard}>
          <div className={styles.statHeader}>
            <span className={styles.statLabel}>Pending Status</span>
            <div className={`${styles.statIcon} ${styles.iconPending}`}>
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                <circle cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="2"/>
                <path d="M12 6v6l4 2" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
              </svg>
            </div>
          </div>
          <div className={styles.statValue}>{stats.pendingApplications}</div>
        </div>

        <div className={styles.statCard}>
          <div className={styles.statHeader}>
            <span className={styles.statLabel}>Profile Strength</span>
            <div className={`${styles.statIcon} ${styles.iconProfile}`}>
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                <circle cx="12" cy="8" r="3" stroke="currentColor" strokeWidth="2"/>
                <path d="M20 21a8 8 0 00-16 0" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
              </svg>
            </div>
          </div>
          <div className={styles.statValue}>{stats.profileStrength}%</div>
        </div>
      </div>

      <div className={styles.dashboardGrid}>
        <div className={styles.quickActions}>
          <h2>Quick Actions</h2>
          <button className={`${styles.actionBtn} ${styles.primary}`} onClick={handleSearchJobs}>
            Search Jobs
          </button>
          <button className={`${styles.actionBtn} ${styles.secondary}`} onClick={handleViewApplications}>
            View Applications
          </button>
          <button className={`${styles.actionBtn} ${styles.secondary}`} onClick={handleUpdateProfile}>
            Update Profile
          </button>
        </div>

        <div className={styles.recentApplications}>
          <h2>Recent Applications</h2>
          <div className={styles.applicationsList}>
            {recentApplications.map(app => (
              <div key={app.id} className={styles.applicationItem}>
                <div className={styles.applicationInfo}>
                  <h3>{app.jobTitle}</h3>
                  <p>{app.company}</p>
                </div>
                <div className={styles.applicationMatch}>
                  <span className={styles.matchScore}>{app.matchScore}%</span>
                  <span className={`${styles.statusBadge} ${styles[app.status]}`}>
                    {app.status}
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      <div className={styles.quickTip}>
        <div className={styles.tipIcon}>💡</div>
        <div className={styles.tipContent}>
          <h3>Quick Tip</h3>
          <p>Update your skills to improve match scores! Adding React and TypeScript experience can increase your match rate by up to 15%.</p>
        </div>
      </div>
    </div>
  )
}

export default JobSeekerDashboard