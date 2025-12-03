# RegWizards -- AI Agents for Automated Policy Compliance

**Track:** Enterprise Agents (Business Workflow Enhancement)

RegWizards is a multi-agent AI system that automatically maps regulations to company policies and rewrites only the relevant ones for instant compliance.

This project was built for the **Google GenAI Kaggle Capstone**.

## Problem

Organizations struggle to keep internal policies aligned with fast-changing regulations.  
Compliance teams manually compare hundreds of policies to laws - a slow, error-prone, expensive process.

**RegWizards automates this entire workflow using AI agents.**

## Why Agents?

This use case requires multiple reasoning steps that no single LLM handles well.  
RegWizards uses specialized agents:

* **Regulation Agent** - retrieves the selected regulation text  
* **Policy Agent** - provides internal policies for evaluation  
* **Rewrite Agent** - rewrites only the policies that need updates  
* **Coordinator Agent** - orchestrates the full compliance workflow  

## Architecture Overview
    User -> Frontend -> Coordinator Agent -> 
      Regulation Agent
      Policy Agent
      Rewrite Agent -> Updated Policies + Compliance Report

Backend: FastAPI/Flask  
LLM: Gemini 2.5 Flash  
Frontend: HTML + JS  
Agents built using Google GenAI Python SDK

### This project demonstrates several core GenAI agent concepts, including:
* Multi-agent workflow (4 agents)
* Sequential agent orchestration
* LLM-powered rewriting using Gemini
* Custom tools for retrieving regulations and policies

## How to Run Locally

### 1. Create `.env`
### 2. Install dependencies
### 3. Run the app
python app.py
### 4. Open in browser
http://127.0.0.1:5000/

## Example Input

**Regulation:** Biometric Data Retention Standard  
**Policies:** Loaded from dataset

**Output includes:**

* Mapped relevant policies  
* Highlighted gaps  
* Rewritten updated policies  
