# Green Calculator

A simple calculator with a fresh green theme.

This project was planned by an OpenAI model and assembled by the Agentic Cloud
demo inside an isolated task workspace.

## Workflow

1. Manager Agent converts the request into a structured specification.
2. Developer Agent creates this branch from a controlled scaffold.
3. QA Agent runs the calculator safety and arithmetic tests.
4. A draft pull request is opened.
5. Human approval in Agentic Cloud triggers the staging deployment.

The application uses FastAPI and stores recent calculation history in a
dedicated PostgreSQL database.

## Test

```bash
python -m unittest discover -s tests -v
```
