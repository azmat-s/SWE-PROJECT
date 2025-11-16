// components/dashboard/Settings.tsx
import { useState } from 'react'

const Settings = () => {
  const [accountSettings, setAccountSettings] = useState({
    email: 'john.doe@email.com',
    fullName: 'John Doe'
  })

  const [notifications, setNotifications] = useState({
    email: true,
    push: false,
    sms: false
  })

  const [darkMode, setDarkMode] = useState(false)

  return (
    <div className="settings-container">
      <div className="page-header">
        <h1>Settings</h1>
        <p>Manage your account preferences</p>
      </div>

      <div className="settings-sections">
        <div className="settings-section">
          <h2>👤 Account Settings</h2>
          <div className="settings-card">
            <div className="form-group">
              <label>Email Address</label>
              <input
                type="email"
                value={accountSettings.email}
                onChange={(e) => setAccountSettings({...accountSettings, email: e.target.value})}
              />
            </div>
            <div className="form-group">
              <label>Full Name</label>
              <input
                type="text"
                value={accountSettings.fullName}
                onChange={(e) => setAccountSettings({...accountSettings, fullName: e.target.value})}
              />
            </div>
            <button className="btn-save">Save Changes</button>
          </div>
        </div>

        <div className="settings-section">
          <h2>🔒 Change Password</h2>
          <div className="settings-card">
            <div className="form-group">
              <label>Current Password</label>
              <input type="password" />
            </div>
            <div className="form-group">
              <label>New Password</label>
              <input type="password" />
            </div>
            <div className="form-group">
              <label>Confirm New Password</label>
              <input type="password" />
            </div>
            <button className="btn-update">Update Password</button>
          </div>
        </div>

        <div className="settings-section">
          <h2>🔔 Notifications</h2>
          <div className="settings-card">
            <div className="toggle-setting">
              <div>
                <h4>Email Notifications</h4>
                <p>Receive job alerts and updates via email</p>
              </div>
              <label className="toggle-switch">
                <input
                  type="checkbox"
                  checked={notifications.email}
                  onChange={(e) => setNotifications({...notifications, email: e.target.checked})}
                />
                <span className="toggle-slider"></span>
              </label>
            </div>
            
            <div className="toggle-setting">
              <div>
                <h4>Push Notifications</h4>
                <p>Get notified about new matches and messages</p>
              </div>
              <label className="toggle-switch">
                <input
                  type="checkbox"
                  checked={notifications.push}
                  onChange={(e) => setNotifications({...notifications, push: e.target.checked})}
                />
                <span className="toggle-slider"></span>
              </label>
            </div>

            <div className="toggle-setting">
              <div>
                <h4>SMS Notifications</h4>
                <p>Receive important updates via SMS</p>
              </div>
              <label className="toggle-switch">
                <input
                  type="checkbox"
                  checked={notifications.sms}
                  onChange={(e) => setNotifications({...notifications, sms: e.target.checked})}
                />
                <span className="toggle-slider"></span>
              </label>
            </div>
          </div>
        </div>

        <div className="settings-section">
          <h2>Appearance</h2>
          <div className="settings-card">
            <div className="toggle-setting">
              <div>
                <h4>Dark Mode</h4>
                <p>Toggle dark mode theme</p>
              </div>
              <label className="toggle-switch">
                <input
                  type="checkbox"
                  checked={darkMode}
                  onChange={(e) => setDarkMode(e.target.checked)}
                />
                <span className="toggle-slider"></span>
              </label>
            </div>
          </div>
        </div>

        <div className="settings-section danger">
          <h2>Danger Zone</h2>
          <div className="settings-card danger-card">
            <p>Deleting your account will permanently remove all your data. This action cannot be undone.</p>
            <button className="btn-danger">Delete Account</button>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Settings