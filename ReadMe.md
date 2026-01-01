# 🔐 QuMail – Quantum-Inspired Secure Messaging System

QuMail is a full-stack, quantum-inspired secure messaging application that demonstrates how simulated Quantum Key Distribution (BB84) can be integrated with classical cryptography to provide end-to-end encryption and decryption in a web-based system.

⚠️ This project uses simulated BB84 QKD for educational and research purposes. No real quantum hardware is involved.

---

## ✨ Features

- Simulated BB84 Quantum Key Distribution
- Dedicated QKD Key Management Service (KMS)
- AES-256-GCM authenticated encryption & decryption
- HKDF-based session key derivation
- FastAPI backend
- React frontend
- End-to-end encrypt → decrypt → recover plaintext
- Swagger API documentation

---

## 🏗️ System Architecture
---
QuMail/
│
├── Qumail/
│ ├── qkd_kms/
│ │ ├── api.py
│ │ ├── bb84.py
│ │ └── kms.py
│ │
│ ├── backend/
│ │ ├── api.py
│ │ └── crypto.py
│ │
│ └── frontend/
│ └── src/App.js
│
└── README.md

---

## 📁 Project Structure


---

## 🚀 How It Works

1. BB84 protocol is simulated to generate a shared secret key.
2. Key reconciliation and privacy amplification produce a 256-bit key.
3. Backend derives a session key using HKDF.
4. Messages are encrypted using AES-GCM.
5. Ciphertext is decrypted to recover original plaintext.

---

## ▶️ Running the Project

### Prerequisites
- Python 3.9+
- Node.js (LTS)
- npm

### Start QKD-KMS
```bash
cd Qumail/qkd_kms
uvicorn api:app --reload --port 8001



cd Qumail/backend
uvicorn api:app --reload --port 8002



cd Qumail/frontend
npm start


🔐 API Endpoints
Backend
Method	Endpoint	Description
POST	/send	Encrypt message
POST	/decrypt	Decrypt message
QKD-KMS
Method	Endpoint	Description
POST	/qkd/generate	Generate QKD key
GET	/qkd/status/{key_id}	Key metadata
POST	/qkd/revoke/{key_id}	Revoke key
🧠 Notes

Not real quantum communication

Quantum-inspired hybrid cryptographic system

Suitable for academic demos, research, and hackathons

👩‍💻 Author

Angel Gupta
AI & ML | Quantum-Inspired Computing | Secure Systems
Smart India Hackathon 2025 – National Level



---

## 2️⃣ Research Paper Abstract 

**Abstract**  
Quantum Key Distribution (QKD) promises theoretically secure communication but faces practical deployment challenges due to hardware limitations. This work presents **QuMail**, a quantum-inspired secure messaging system that integrates a simulated BB84 QKD protocol with classical cryptographic primitives. The system employs key reconciliation and privacy amplification to generate shared secret keys, which are further used for AES-256-GCM authenticated encryption through HKDF-derived session keys. Implemented as a full-stack web application using FastAPI and React, QuMail demonstrates how quantum-inspired key management can be practically integrated into modern secure communication systems. The proposed architecture serves as an educational and research-oriented model for hybrid cryptographic systems bridging quantum concepts with real-world applications.

---

## 3️⃣ Resume Bullet Points (Strong & Correct)

- Designed and implemented a **quantum-inspired secure messaging system** using simulated BB84 Quantum Key Distribution.
- Built a **QKD-based Key Management Service** with reconciliation, privacy amplification, and key lifecycle management.
- Integrated **AES-256-GCM encryption and decryption** using HKDF-derived session keys.
- Developed a **full-stack web application** using FastAPI and React for secure message transmission.
- Demonstrated hybrid cryptographic architecture suitable for research, academic demos, and SIH-level projects.


---

## 5️⃣ One-Line Project Description 

> Built a quantum-inspired secure messaging system using simulated BB84 QKD integrated with AES-GCM encryption in a full-stack web application.

---

## ✅ You now have

- ✔ GitHub-ready README  
- ✔ Research paper abstract  
- ✔ Resume bullets  
- ✔ SIH demo explanation  
- ✔ Correct technical positioning  

If you want next (optional):
- Architecture diagram (PNG/SVG)
- PPT slides
- Security analysis section
- Post-quantum upgrade (Kyber)

Just tell me.
