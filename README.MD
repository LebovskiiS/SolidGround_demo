# Solid Ground - PTSD Support Application

## Overview
**Solid Ground** is a Desktop application designed to support individuals with **PTSD** (Post-Traumatic Stress Disorder).  
The application provides various features to help users manage their condition, offering tools like emergency assistance, therapeutic resources, and communication with mental health professionals.

This repository contains the **API/backend** part of the project, which serves as the foundation for the mobile application.

---

## Features

- **User Authentication**: Secure registration and login system.
- **User Profiles**: Personalized profiles with PTSD-related information.
- **Emergency Assistance**: Quick access to help during panic attacks or PTSD episodes.
- **Alarm System**: Configurable alarm scenarios that can notify emergency contacts and therapists.
- **Therapeutic Resources**: Access to calming music and other therapeutic resources.
- **Chat Support**: Communication with AI assistant (GPT) for immediate support.
- **Therapist Connection**: Integration with mental health professionals.

---

## Technical Stack

- **Backend**: Django REST Framework.
- **Database**: PostgreSQL.
- **Real-time Communication**: Django Channels with WebSockets.
- **AI Integration**: OpenAI GPT for chat support.
- **Authentication**: Token-based authentication.

---

## Project Structure

- **`main`**: Core application functionality and user management.
- **`event`**: Alarm system and emergency response features.
- **`chat`**: Real-time communication and GPT integration.

---

## API Documentation

The **API documentation** is available in the `api_documentation.md` file.  
It provides detailed information about all available endpoints and their usage.

---

## Note

This repository is for **demonstration purposes only** and is part of a portfolio.  
It is intended to showcase the application's **architecture** and **coding style**, not to be run or deployed.  
The actual working application is available on the author's personal website.

The repository contains all the code and configuration files to demonstrate the structure and implementation of the application, but it is **not set up for direct execution or deployment**.