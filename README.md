# Cyber Tabletop - Turn-Based Incident Response Platform

A production-ready turn-based cyber incident response tabletop platform for running training scenarios. Built with FastAPI (backend) and React + TypeScript (frontend), using stateless HTTP polling instead of websockets.

## 🎯 Features

- **GM Console**: Game Master interface for managing scenarios, phases, and scoring
- **Team Decision Pad**: Interface for Red/Blue teams to submit decisions
- **Audience View**: Public scoreboard for displaying game progress
- **Polling-Based**: All real-time updates use HTTP polling (no websockets)
- **Turn-Based Phases**: Structured phase progression with state management

## 🏗️ Architecture

- **Backend**: FastAPI + SQLAlchemy + PostgreSQL
- **Frontend**: React + TypeScript + Vite + Tailwind CSS
- **Database**: PostgreSQL with Alembic migrations
- **Auth**: JWT-based authentication for GM users

## 📋 Prerequisites

- Docker and Docker Compose (for containerized setup)
- OR Python 3.11+ and Node.js 18+ (for local development)

## 🚀 Quick Start with Docker

1. **Clone and navigate to the project**:
   ```bash
   cd cybertabletop
   ```

2. **Start services**:
   ```bash
   docker-compose -f docker-compose.dev.yml up --build
   ```

3. **Initialize database and seed data** (in a new terminal):
   ```bash
   # Run migrations
   docker-compose -f docker-compose.dev.yml exec backend alembic upgrade head
   
   # Seed initial data
   docker-compose -f docker-compose.dev.yml exec backend python seed_data.py
   ```

4. **Access the application**:
   - Frontend: http://localhost:5173
   - Backend API: http://localhost:8001
   - API Docs: http://localhost:8001/docs

## 🔧 Local Development Setup

### Backend Setup

1. **Create virtual environment**:
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env with your database URL and JWT secret
   ```

4. **Run database migrations**:
   ```bash
   alembic upgrade head
   ```

5. **Seed initial data**:
   ```bash
   python seed_data.py
   ```

6. **Start the server**:
   ```bash
   uvicorn app.main:app --reload
   ```

### Frontend Setup

1. **Install dependencies**:
   ```bash
   cd frontend
   npm install
   ```

2. **Start development server**:
   ```bash
   npm run dev
   ```

3. **Access the app**: http://localhost:5173

## 🔐 Default Credentials

After seeding data, you can log in as GM with:
- **Username**: `admin`
- **Password**: `admin123`

**⚠️ Change these credentials in production!**

## 📖 Usage Guide

### For Game Masters

1. **Login**: Navigate to `/gm/login` and log in with GM credentials
2. **Create Game**: Select a scenario and create a new game
3. **Start Game**: Click "Start Game" to begin the first phase
4. **Manage Phases**:
   - "Open for Decisions": Allow teams to submit decisions
   - "Lock Decisions": Close decision submission
   - "Resolve Phase": Review and score decisions
   - "Complete & Next Phase": Move to the next phase
5. **Share Codes**: Copy and share team codes and audience URL

### For Team Players

1. **Join**: Navigate to `/play/join`
2. **Enter Code**: Enter your team code and display name
3. **View Phase**: See current phase briefing, objectives, and artifacts
4. **Submit Decision**: When phase is open, select actions and submit justification
5. **View Results**: See your submitted decision and wait for resolution

### For Audience

1. **View Scoreboard**: Navigate to `/audience/{gameIdentifier}`
2. **Monitor Progress**: Watch real-time scores and phase updates

## 🗄️ Database Schema

### Core Models

- **GMUser**: Game Master accounts
- **Scenario**: Reusable scenario templates
- **ScenarioPhase**: Phases within a scenario
- **Artifact**: Evidence items (logs, screenshots, etc.)
- **Game**: Active game instances
- **Team**: Teams within a game (Red, Blue, etc.)
- **Player**: Individual players
- **PhaseDecision**: Team decisions for each phase
- **ScoreEvent**: Scoring history

## 🔄 Phase State Machine

Each phase progresses through these states:
1. `not_started` → Initial state
2. `briefing` → GM presents phase briefing
3. `open_for_decisions` → Teams can submit decisions
4. `decision_lock` → Decisions are locked
5. `resolution` → GM reviews and scores
6. `complete` → Phase finished

## 📡 API Endpoints

### Authentication
- `POST /auth/login` - GM login

### Scenarios
- `GET /scenarios` - List scenarios (GM only)
- `GET /scenarios/{id}` - Get scenario details (GM only)

### Games
- `POST /games` - Create game (GM only)
- `GET /games` - List games (GM only)
- `GET /games/{id}` - Get game details (GM only)
- `POST /games/{id}/start` - Start game
- `POST /games/{id}/phase/open_for_decisions` - Open phase for decisions
- `POST /games/{id}/phase/lock_decisions` - Lock decisions
- `POST /games/{id}/phase/resolve` - Enter resolution phase
- `POST /games/{id}/phase/complete_and_next` - Complete phase and move to next
- `POST /games/{id}/end` - End game

### Players
- `POST /join` - Join game with team code
- `GET /games/{id}/player/{player_id}/state` - Get player state (polling endpoint)

### Decisions
- `POST /games/{id}/phases/{phase_id}/decisions` - Submit decision
- `GET /games/{id}/phases/{phase_id}/decisions` - Get all decisions (GM only)
- `POST /games/{id}/phases/{phase_id}/decisions/{decision_id}/score` - Score decision (GM only)

### Scoreboard
- `GET /games/{identifier}/scoreboard` - Get public scoreboard

## 🧪 Testing

Run the seed script to create test data:
```bash
python backend/seed_data.py
```

This creates:
- 1 GM user (admin/admin123)
- 1 Scenario with 3 phases
- 5 Artifacts distributed across phases

## 🐳 Docker Commands

**Start services**:
```bash
docker-compose -f docker-compose.dev.yml up
```

**Stop services**:
```bash
docker-compose -f docker-compose.dev.yml down
```

**View logs**:
```bash
docker-compose -f docker-compose.dev.yml logs -f backend
```

**Run migrations**:
```bash
docker-compose -f docker-compose.dev.yml exec backend alembic upgrade head
```

**Seed data**:
```bash
docker-compose -f docker-compose.dev.yml exec backend python seed_data.py
```

## 📝 Environment Variables

### Backend (.env)
```
DATABASE_URL=postgresql://cybertabletop:cybertabletop@db:5432/cybertabletop
JWT_SECRET_KEY=your-secret-key-change-in-production
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24
```

### Frontend
Set `VITE_API_URL` if running frontend separately (defaults to `/api` proxy)

## 🔄 Polling Intervals

- **GM Console**: 5 seconds
- **Team Decision Pad**: 8 seconds
- **Audience View**: 8 seconds

These can be adjusted in the respective React components.

## 🛠️ Development

### Creating Migrations

```bash
cd backend
alembic revision --autogenerate -m "Description"
alembic upgrade head
```

### Project Structure

```
cybertabletop/
├── backend/
│   ├── app/
│   │   ├── routers/      # API route handlers
│   │   ├── models.py     # SQLAlchemy models
│   │   ├── schemas.py    # Pydantic schemas
│   │   ├── auth.py       # Authentication logic
│   │   ├── database.py   # Database setup
│   │   └── main.py       # FastAPI app
│   ├── alembic/          # Database migrations
│   ├── seed_data.py      # Initial data seeding
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── pages/        # React page components
│   │   ├── api/          # API client
│   │   └── types.ts      # TypeScript types
│   └── package.json
└── docker-compose.yml
```

## 📄 License

This project is provided as-is for educational and training purposes.

## 🤝 Contributing

This is a production-ready starter template. Feel free to extend it with:
- Additional scenario templates
- More artifact types
- Enhanced scoring mechanisms
- Real-time notifications (while maintaining polling architecture)
- Export/import functionality
- Analytics and reporting

---

**Built with ❤️ for cybersecurity training**

