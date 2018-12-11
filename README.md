BAB - Security Control for Database Access
==========================================


## Short description
- Control panel for security updates and requirements for a company with sensitive data. 
- Purpose: hightlighting security weakpoints in a network of 100+ endpoint machines to (once implemented in a company) control access to sensitive data.
- Three-week project of Anna Wyss and Pascal Rüegger at Propulsion Academy.
- In cooperation with RepRisk AG. 


## Functionality

**Agent**
- Can be installed locally on endpoint machines
- Collects data on status of security updates of endpoint machine
- Sends collected data to control panel
- Recieves and displays status report

**Control Panel (Backend and Frontend)**
- Stores security standards
- Compares incoming agent data with security standards
- Provides an overview and filter functions of the security status of all registered endpoint machines


## Built with

**Agent**
- Javascript
- Electron.js, 
- Vue.js

**Backend**
- Python
- Django REST
- Docker

**Frontend** 
- Javascript
- React
- Redux
- Docker


## Authors
Pascal Rüegger  
Anna Wyss


