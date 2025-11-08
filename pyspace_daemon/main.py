from fastapi import FastAPI
import uvicorn

app = FastAPI(
    title="PySpace Daemon",
    description="Background service for PySpace environment management",
)


@app.get("/")
def read_root():
    return {"message": "PySpace Daemon is running"}


@app.get("/workspaces")
def list_workspaces():
    # TODO: implement
    return {"workspaces": []}


@app.post("/workspaces")
def create_workspace(name: str):
    # TODO: implement
    return {"message": f"Workspace {name} created"}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
