from typing import List

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select

from schemas import TaskCreate, TaskResponse
from database import get_db
from models import Task


app = FastAPI(title="ToDo List")


@app.get("/tasks/", response_model=List[TaskResponse])
def read_tasks(db: Session = Depends(get_db)):
    result = db.execute(select(Task))
    tasks = result.scalars().all()

    task_responses = [
        TaskResponse(
            id=task.id,
            title=task.title,
            description=task.description,
            done=task.done
        ) for task in tasks
    ]

    return task_responses


@app.post("/tasks/", response_model=TaskCreate)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    db_task = Task(title=task.title, description=task.description)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)

    task_create = TaskCreate(
        title=db_task.title,
        description=db_task.description
    )

    return task_create