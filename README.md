# SYSC 4810 A Assignment - justInvest System

Kareem Kaddoura
101140255 

## Description

The justInvest Portfolio Management System is a user authentication and access control system prototype that implements an Role-Based Access Control System (RBAC), where user priveleges and permitted operations are seperated depending on the role they have chosen upon user-account creation.

Users can register accouts and log in to the system, where a proactive security system is in place to ensure unqiue username-creation and implement proper and secure hashing algorithms to ensure the secure storage of the user's credentials. The system uses hashlib's pbkdf2_hmac() in combination with the 'SHA-256' hashing algorithm to hash a user's password, along with salting and iterated hashing to make the resulting 64-byte password hash as secure as possible.

## Instructions

1. Execute `python3 main.py` on the VM terminal.