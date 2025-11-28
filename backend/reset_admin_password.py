#!/usr/bin/env python3
"""
Direct script to reset admin password.
Can be run directly or via docker exec.

Usage:
    python reset-admin-password-direct.py <new_password>
    OR
    docker exec <backend_container> python reset-admin-password-direct.py <new_password>
"""
import sys
import os
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import GMUser
from app.auth import get_password_hash

def reset_admin_password(new_password: str):
    if len(new_password) < 6:
        print("❌ Password must be at least 6 characters long")
        return False
    
    db: Session = SessionLocal()
    try:
        # Find admin user
        admin_user = db.query(GMUser).filter(GMUser.username == 'admin').first()
        if not admin_user:
            print("❌ Admin user not found in database")
            print("You may need to run seed_data.py first")
            return False
        
        # Update password
        admin_user.password_hash = get_password_hash(new_password)
        db.commit()
        print("✓ Admin password reset successfully")
        print("")
        print("You can now login with:")
        print("  Username: admin")
        return True
    except Exception as e:
        print(f"❌ Error resetting password: {e}")
        db.rollback()
        return False
    finally:
        db.close()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python reset-admin-password-direct.py <new_password>")
        sys.exit(1)
    
    new_password = sys.argv[1]
    success = reset_admin_password(new_password)
    sys.exit(0 if success else 1)

