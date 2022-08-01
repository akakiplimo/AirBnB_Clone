#!/usr/bin/python3
"""Defines User class inherited from BaseModel"""
from models.base_model import BaseModel


class User(BaseModel):
    """Public class attributes"""
    email = ""
    password = ""
    first_name = ""
    last_name = ""
