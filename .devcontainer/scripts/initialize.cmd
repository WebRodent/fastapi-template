@echo off

rem Check if .devcontainer\devcontainer.env exists, and create it if not
if not exist ".devcontainer\devcontainer.env" (
    echo "devcontainer.env not found, creating one..."
    copy ".devcontainer\devcontainer.env.example" ".devcontainer\devcontainer.env"
)