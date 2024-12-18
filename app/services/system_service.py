def get_system_status():
    # Simula estado de sistemas
    return [{"id": 1, "name": "Presurización", "status": "Activo"}]

def send_command(system_id, device, command):
    # Simula el envío de un comando
    return {"system_id": system_id, "device": device, "command": command, "status": "Enviado"}
