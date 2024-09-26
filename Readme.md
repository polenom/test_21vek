# Project Setup and Launch Guide

This guide will walk you through setting up the environment and launching the project using Docker.

---

## Step 1: Configure Environment Variables

1. Copy the sample environment configuration file to create the actual `.env` file:
   
   ```bash
   cp .env.sample .env
   ```
   
## Step 2: Build and Start Docker Containers

1. To build and run all necessary containers, use the following command: file:
   
   ```bash
   docker compose up -d
   ```

## Step 3: Access Project Documentation

1. Once the containers are up and running, you can access the project documentation at:
   
   [Project Docs](http://localhost:8000/docs)