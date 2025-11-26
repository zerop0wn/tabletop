from app.database import SessionLocal
from app.models import GMUser
from app.auth import verify_password, authenticate_user

db = SessionLocal()

try:
    user = db.query(GMUser).filter(GMUser.username == 'admin').first()
    print(f'User found: {user is not None}')
    if user:
        print(f'Password hash: {user.password_hash[:50]}...')
        try:
            result = verify_password('admin123', user.password_hash)
            print(f'Password verification: {result}')
        except Exception as e:
            print(f'Password verification error: {e}')
            import traceback
            traceback.print_exc()
        
        # Test authenticate_user
        try:
            auth_user = authenticate_user(db, 'admin', 'admin123')
            print(f'Authenticate user result: {auth_user is not None}')
        except Exception as e:
            print(f'Authenticate user error: {e}')
            import traceback
            traceback.print_exc()
finally:
    db.close()

