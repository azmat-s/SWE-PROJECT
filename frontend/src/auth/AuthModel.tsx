import { useState, type FormEvent } from 'react'
import { useNavigate } from 'react-router-dom'

interface AuthModalProps {
  mode: 'login' | 'signup'
  onClose: () => void
  onSwitchMode: () => void
}

const AuthModal = ({ mode, onClose, onSwitchMode }: AuthModalProps) => {
  const navigate = useNavigate()
  const [userType, setUserType] = useState<'recruiter' | 'jobseeker'>('recruiter')
  const [showPassword, setShowPassword] = useState(false)
  const [rememberMe, setRememberMe] = useState(false)
  const [formData, setFormData] = useState({
    fullName: '',
    email: '',
    companyName: '',
    companyWebsite: '',
    password: '',
    confirmPassword: '',
    resumeFile: null as File | null
  })

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault()
    console.log('Form submitted:', { ...formData, userType, rememberMe })
    navigate('/dashboard')
  }

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    })
  }

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFormData({
        ...formData,
        resumeFile: e.target.files[0]
      })
    }
  }

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="auth-modal-content" onClick={(e) => e.stopPropagation()}>
        <button className="modal-close" onClick={onClose}>×</button>
        
        <div className="auth-modal-container">
          <div className="auth-icon-container">
            <svg width="32" height="32" viewBox="0 0 24 24" fill="white">
              <path d="M19 3h-1V1h-2v2H8V1H6v2H5c-1.11 0-1.99.9-1.99 2L3 19c0 1.1.89 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm0 16H5V8h14v11zM7 10h5v5H7z"/>
            </svg>
          </div>

          {mode === 'login' ? (
            <>
              <h2 className="auth-main-title">MatchWise</h2>
              <p className="auth-tagline">AI-driven Job Matching Platform</p>
            </>
          ) : (
            <>
              <h2 className="auth-main-title">Create Account</h2>
              <p className="auth-tagline">Join MatchWise today</p>
            </>
          )}

          <div className="auth-toggle">
            <button 
              className={`toggle-btn ${userType === 'recruiter' ? 'active' : ''}`}
              onClick={() => setUserType('recruiter')}
              type="button"
            >
              Recruiter
            </button>
            <button 
              className={`toggle-btn ${userType === 'jobseeker' ? 'active' : ''}`}
              onClick={() => setUserType('jobseeker')}
              type="button"
            >
              Job Seeker
            </button>
          </div>

          <form onSubmit={handleSubmit} className="auth-form">
            {mode === 'signup' && (
              <div className="form-field">
                <label className="field-label">Full Name</label>
                <input
                  type="text"
                  name="fullName"
                  placeholder="John Doe"
                  className="auth-input"
                  value={formData.fullName}
                  onChange={handleInputChange}
                  required
                />
              </div>
            )}

            <div className="form-field">
              <label className="field-label">Email</label>
              <input
                type="email"
                name="email"
                placeholder={mode === 'login' ? 'your@email.com' : 'your@email.com'}
                className="auth-input"
                value={formData.email}
                onChange={handleInputChange}
                required
              />
            </div>

            {mode === 'signup' && userType === 'recruiter' && (
              <>
                <div className="form-field">
                  <label className="field-label">Company Name</label>
                  <input
                    type="text"
                    name="companyName"
                    placeholder="Acme Inc."
                    className="auth-input"
                    value={formData.companyName}
                    onChange={handleInputChange}
                    required
                  />
                </div>
                <div className="form-field">
                  <label className="field-label">Company Website</label>
                  <input
                    type="url"
                    name="companyWebsite"
                    placeholder="https://example.com"
                    className="auth-input"
                    value={formData.companyWebsite}
                    onChange={handleInputChange}
                    required
                  />
                </div>
              </>
            )}

            {mode === 'signup' && userType === 'jobseeker' && (
              <div className="form-field">
                <label className="field-label">Upload Resume (PDF)</label>
                <div className="file-upload-container">
                  <input
                    type="file"
                    id="resume-upload"
                    accept=".pdf"
                    onChange={handleFileChange}
                    className="file-input-hidden"
                  />
                  <label htmlFor="resume-upload" className="file-upload-label">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                      <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
                      <polyline points="17 8 12 3 7 8"/>
                      <line x1="12" y1="3" x2="12" y2="15"/>
                    </svg>
                    <span>{formData.resumeFile ? formData.resumeFile.name : 'Choose file'}</span>
                  </label>
                </div>
              </div>
            )}

            <div className="form-field">
              <label className="field-label">Password</label>
              <div className="password-input-wrapper">
                <input
                  type={showPassword ? 'text' : 'password'}
                  name="password"
                  placeholder="••••••••"
                  className="auth-input"
                  value={formData.password}
                  onChange={handleInputChange}
                  required
                />
                {mode === 'login' && (
                  <button
                    type="button"
                    className="password-toggle"
                    onClick={() => setShowPassword(!showPassword)}
                  >
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                      {showPassword ? (
                        <>
                          <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/>
                          <circle cx="12" cy="12" r="3"/>
                        </>
                      ) : (
                        <>
                          <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"/>
                          <line x1="1" y1="1" x2="23" y2="23"/>
                        </>
                      )}
                    </svg>
                  </button>
                )}
              </div>
            </div>

            {mode === 'signup' && (
              <div className="form-field">
                <label className="field-label">Confirm Password</label>
                <input
                  type="password"
                  name="confirmPassword"
                  placeholder="••••••••"
                  className="auth-input"
                  value={formData.confirmPassword}
                  onChange={handleInputChange}
                  required
                />
              </div>
            )}

            {mode === 'login' && (
              <div className="form-options">
                <label className="checkbox-label">
                  <input 
                    type="checkbox"
                    checked={rememberMe}
                    onChange={(e) => setRememberMe(e.target.checked)}
                  />
                  <span>Remember me</span>
                </label>
                <a href="#" className="forgot-password">Forgot Password?</a>
              </div>
            )}

            <button type="submit" className="submit-btn">
              {mode === 'login' ? 'Login' : 'Create Account'}
            </button>
          </form>

          <div className="auth-footer">
            <span className="switch-text">
              {mode === 'login' ? "Don't have an account? " : "Already have an account? "}
            </span>
            <button onClick={onSwitchMode} className="switch-link">
              {mode === 'login' ? 'Sign up' : 'Login'}
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}

export default AuthModal