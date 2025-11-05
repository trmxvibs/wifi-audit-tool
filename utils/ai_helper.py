def suggest_network(networks):
    """
    Analyzes a list of network dictionaries and prints security recommendations.
    
    NOTE: This function currently expects a Python list of networks,
    but scan.py no longer provides this. To use this, scan.py
    must be modified to parse airodump-ng output into a list.
    """
    print("\nAI Recommendations:")
    found_weakness = False
    
    for net in networks:
        if net["security"] == "OPEN":
            print(f"- {net['ssid']} is an OPEN network and may be insecure.")
            found_weakness = True
        elif net["security"] == "WEP":
            print(f"- {net['ssid']} uses WEP, which is outdated and highly vulnerable.")
            found_weakness = True
            
    if not found_weakness:
        print("- All found networks appear to use modern security (WPA2/WPA3).")
