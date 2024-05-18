import asyncio
from snmp_agent import Server, SNMPRequest, SNMPResponse, VariableBinding, OctetString, TimeTicks, Integer

# Define a dictionary to map OIDs to their corresponding data and data types
data_map = {
    '1.3.6.1.2.1.1.1.0': ('System', OctetString),  # System description
    '1.3.6.1.2.1.1.3.0': (100, TimeTicks),          # Uptime
    '1.3.6.1.2.1.2.2.1.1.1': (1, Integer),         # Interface index
    '1.3.6.1.2.1.2.2.1.2.1': ('fxp0', OctetString),   # Interface name
    # ... Add more OIDs and data as needed
}


async def handle_request(req: SNMPRequest) -> SNMPResponse:
    """
    Handles incoming SNMP requests and returns the corresponding data.
    """

    response_vbs = []
    for oid, (value, data_type) in data_map.items():
        if oid in req.var_binds:
            try:
                if callable(value):
                    value = value(oid)  # Call function for dynamic data retrieval
                response_vbs.append(VariableBinding(oid, data_type(value)))
            except Exception as e:
                print(f"Error retrieving data for OID {oid}: {e}")
                # Handle errors appropriately (e.g., return SNMP error code)

    return req.create_response(response_vbs)


async def main():
    """
    Starts the SNMP server.
    """

    server = Server(handler=handle_request, host='0.0.0.0', port=161)
    await server.start()
    while True:
        await asyncio.sleep(3600)  # Optional: Check for server status periodically


if __name__ == '__main__':
    asyncio.run(main())
