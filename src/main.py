from fastapi import FastAPI
import models, database
import users, roles, permissions, role_permissions

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

app.include_router(users.router)
app.include_router(roles.router)
app.include_router(permissions.router)
app.include_router(role_permissions.router)
