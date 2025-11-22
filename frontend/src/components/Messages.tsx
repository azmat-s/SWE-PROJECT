// components/dashboard/Messages.tsx
import { useState } from 'react'

const Messages = () => {
  const [conversations] = useState([
    {
      id: 1,
      name: 'Sarah Johnson',
      role: 'Senior Frontend Developer',
      message: 'Thank you for considering my application!',
      time: '2m ago',
      unread: true
    },
    {
      id: 2,
      name: 'Michael Chen',
      message: 'I would love to discuss the role further',
      time: '1h ago',
      unread: false
    },
    {
      id: 3,
      name: 'Emily Rodriguez',
      message: 'When would be a good time for an interview?',
      time: '3h ago',
      unread: true
    },
    {
      id: 4,
      name: 'David Kim',
      message: 'I have experience with similar projects',
      time: '1d ago',
      unread: false
    }
  ])

  const [selectedConversation, setSelectedConversation] = useState(conversations[0])
  const [messageInput, setMessageInput] = useState('')

  const messages = [
    {
      sender: 'Sarah Johnson',
      content: "Hi! I applied for the Senior Frontend Developer position.",
      time: '10:30 AM',
      isMe: false
    },
    {
      sender: 'You',
      content: "Hello Sarah! Thank you for applying. Your profile looks impressive.",
      time: '10:32 AM',
      isMe: true
    },
    {
      sender: 'Sarah Johnson',
      content: "Thank you! I have 7 years of experience with React and TypeScript.",
      time: '10:35 AM',
      isMe: false
    },
    {
      sender: 'You',
      content: "Great! Would you be available for a technical interview next week?",
      time: '10:40 AM',
      isMe: true
    },
    {
      sender: 'Sarah Johnson',
      content: "Yes, I am available. What day works best for you?",
      time: '10:42 AM',
      isMe: false
    },
    {
      sender: 'Sarah Johnson',
      content: "Thank you for considering my application!",
      time: '10:45 AM',
      isMe: false
    }
  ]

  return (
    <div className="messages-container">
      <div className="page-header">
        <h1>Messages</h1>
        <p>Communicate with candidates</p>
      </div>

      <div className="messages-layout">
        <div className="conversations-list">
          <div className="search-bar">
            <input type="text" placeholder="Search messages..." />
          </div>
          
          <div className="conversations">
            {conversations.map(conv => (
              <div
                key={conv.id}
                className={`conversation-item ${selectedConversation.id === conv.id ? 'active' : ''} ${conv.unread ? 'unread' : ''}`}
                onClick={() => setSelectedConversation(conv)}
              >
                <div className="conversation-avatar">
                  {conv.name.split(' ').map(n => n[0]).join('')}
                </div>
                <div className="conversation-details">
                  <div className="conversation-header">
                    <h4>{conv.name}</h4>
                    <span className="time">{conv.time}</span>
                  </div>
                  <p className="last-message">{conv.message}</p>
                </div>
                {conv.unread && <span className="unread-badge">●</span>}
              </div>
            ))}
          </div>
        </div>

        <div className="conversation-view">
          <div className="conversation-header">
            <div className="header-info">
              <div className="avatar-large">
                {selectedConversation.name.split(' ').map(n => n[0]).join('')}
              </div>
              <div>
                <h3>{selectedConversation.name}</h3>
                <p>Senior Frontend Developer</p>
              </div>
            </div>
            <button className="btn-ai-suggestions">🤖 AI Suggestions</button>
          </div>

          <div className="messages-area">
            {messages.map((msg, index) => (
              <div key={index} className={`message ${msg.isMe ? 'me' : 'them'}`}>
                <div className="message-content">
                  <p>{msg.content}</p>
                  <span className="message-time">{msg.time}</span>
                </div>
              </div>
            ))}
          </div>

          <div className="message-input-area">
            <input
              type="text"
              placeholder="Type a message..."
              value={messageInput}
              onChange={(e) => setMessageInput(e.target.value)}
            />
            <button className="send-btn">Send</button>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Messages