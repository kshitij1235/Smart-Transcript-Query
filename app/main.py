from fastapi import FastAPI, Depends
import httpx
from typing import List
from app.api.router import router

app = FastAPI(
    title="Smart Transcript Query System with FastAPI & Gemini API",
    description="""This project aims to build an AI-powered transcript query system that allows users to 
    efficiently extract insights from video transcripts. 
    Using FastAPI and the Gemini API, the system enables batch processing,
    caching, and long-context handling to ensure fast, accurate, and scalable responses.""",
    version="1.0.0",
)

app.include_router(router)