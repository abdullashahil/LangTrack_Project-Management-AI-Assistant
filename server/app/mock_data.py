def get_mock_data():
    return {
        "projects": [
            {
                "id": "proj-001",
                "name": "Alpha Website",
                "status": "Behind Schedule",
                "start_date": "2023-07-01",
                "deadline": "2023-09-30",
                "progress": 45,
                "team": ["alice", "bob"],
                "description": "Company website redesign project"
            },
            {
                "id": "proj-002",
                "name": "Beta Mobile",
                "status": "On Track",
                "start_date": "2023-08-15",
                "deadline": "2023-11-20",
                "progress": 20,
                "team": ["bob", "charlie"],
                "description": "New mobile app development"
            }
        ],
        "tasks": [
            {
                "name": "Design Homepage",
                "status": "Completed",
                "assignee": "alice",
                "project": "Alpha Website"
            },
            {
                "name": "API Integration",
                "status": "In Progress",
                "assignee": "bob",
                "project": "Alpha Website"
            },
            {
                "name": "User Authentication",
                "status": "Pending",
                "assignee": "charlie",
                "project": "Beta Mobile"
            },
            {
                "name": "Database Schema",
                "status": "Pending",
                "assignee": "bob",
                "project": "Beta Mobile"
            }
        ],
        "team": [
            {
                "id": "alice",
                "name": "Alice",
                "role": "Designer",
                "task_count": 1
            },
            {
                "id": "bob",
                "name": "Bob",
                "role": "Developer",
                "task_count": 3
            },
            {
                "id": "charlie",
                "name": "Charlie",
                "role": "Developer",
                "task_count": 1
            }
        ]
    }