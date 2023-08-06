import argparse
import pysolarfocus as sf

from pymodbus.client.sync import ModbusTcpClient as ModbusClient


def run(host):
    client =  ModbusClient(host, port=502)
    #client.connect()

    rr = client.read_input_registers(1100, 7)
    print(f"Heizkreis: {rr.registers}")

    rr = client.read_input_registers(1900, 6)
    print(f"Puffer: {rr.registers}")

    rr = client.read_input_registers(500, 3)
    print(f"Boiler: {rr.registers}")

    rr = client.read_input_registers(2300, 31)
    print(f"Wärmepumpe: {rr.registers}")


    bits = (rr.registers[7] << 16) + rr.registers[8]

    bits_in_kwh=float(bits/1000)
   # s = struct.pack('>l', bits)
    #final = struct.unpack('>f', s)[0]
    print(f"Gesamt: {bits} Wh")
    print(f"Gesamt: {bits_in_kwh} kWh")

    rr = client.read_input_registers(2500, 10)
    print(f"PV: {rr.registers}")

    solarfocus = sf.SolarfocusAPI(client, 1)

    solarfocus.update()

    value=solarfocus.hc1_supply_temp
    print(f"vorlauf: {value}")


def main():
    #parser = argparse.ArgumentParser(description="Solarfocus Heating System")
    #parser.add_argument("--host", help="Local Solarfocus host (or IP)")
    #args = parser.parse_args()

    run( "172.16.1.17" )#args.host)


if __name__ == "__main__":
    main()