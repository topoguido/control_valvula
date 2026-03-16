Control de valvula con ESP-01 y A4988

Cableado basico
- ESP-01 GPIO2 -> A4988 STEP
- ESP-01 GPIO0 -> A4988 DIR
- ESP-01 3V3 -> A4988 VDD
- ESP-01 GND -> A4988 GND

Habilitacion del driver (fijo)
- A4988 RESET y SLEEP unidos y a VDD
- A4988 ENABLE a GND (activo en LOW)

Microstepping
- MS1, MS2, MS3 a GND para full step
- Los pasos enviados en los endpoints son pasos del driver

Endpoints
- /valve_open?steps=N
- /valve_close?steps=N

Notas
- GPIO0 y GPIO2 deben quedar en HIGH al boot para arrancar normal
- Evitar pulls fuertes a LOW en esos pines
