from sqlalchemy import Column, String, DateTime, Integer
from datetime import datetime, timedelta
from shared.database.database import Base

class OAuthState(Base):
    """класс для состояния OAuth"""
    __tablename__ = "oauth_states"
    
    id = Column(Integer, primary_key=True, index=True)
    state = Column(String(100), unique=True, index=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=False)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.expires_at:
            self.expires_at = datetime.utcnow() + timedelta(minutes=10)
    
    def is_expired(self) -> bool:
        return datetime.utcnow() > self.expires_at