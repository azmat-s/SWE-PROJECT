import { NavLink, useNavigate } from 'react-router-dom'
import '../styles/dashboard.css'

interface SidebarProps {
  userType: 'recruiter' | 'jobseeker'
}

const Sidebar = ({ userType }: SidebarProps) => {
  const navigate = useNavigate()

  const handleLogout = () => {
    navigate('/login')
  }

  const getNavigationItems = () => {
    if (userType === 'recruiter') {
      return [
        { path: '/dashboard/overview', label: 'Dashboard', icon: '📊' },
        { path: '/dashboard/view-jobs', label: 'View Jobs', icon: '💼' },
        { path: '/dashboard/post-job', label: 'Post Job', icon: '➕' },
        { path: '/dashboard/messages', label: 'Messages', icon: '💬' },
        { path: '/dashboard/settings', label: 'Settings', icon: '⚙️' }
      ]
    } else {
      return [
        { path: '/dashboard/overview', label: 'Dashboard', icon: '📊' },
        { path: '/dashboard/search-jobs', label: 'Search Jobs', icon: '🔍' },
        { path: '/dashboard/my-applications', label: 'My Applications', icon: '📄' },
        { path: '/dashboard/profile', label: 'Profile', icon: '👤' },
        { path: '/dashboard/messages', label: 'Messages', icon: '💬' },
        { path: '/dashboard/settings', label: 'Settings', icon: '⚙️' }
      ]
    }
  }

  return (
    <div className="sidebar">
      <div className="sidebar-header">
        <div className="logo-container">
          <div className="logo-icon">M</div>
          <div>
            <h2 className="sidebar-title">MatchWise</h2>
            <p className="sidebar-subtitle">AI-driven Job Matching</p>
          </div>
        </div>
      </div>

      <nav className="sidebar-nav">
        {getNavigationItems().map(item => (
          <NavLink
            key={item.path}
            to={item.path}
            className={({ isActive }) =>
              isActive ? 'sidebar-link active' : 'sidebar-link'
            }
          >
            <span className="sidebar-icon">{item.icon}</span>
            {item.label}
          </NavLink>
        ))}
      </nav>

      <button className="logout-btn" onClick={handleLogout}>
        <span className="sidebar-icon">🚪</span>
        Logout
      </button>
    </div>
  )
}

export default Sidebar