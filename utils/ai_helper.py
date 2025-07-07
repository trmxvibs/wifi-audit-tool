def suggest_network(networks):
    print("\nAI Recommendations:")
    found = False
    for net in networks:
        if net["security"] == "OPEN":
            print(f"- {net['ssid']} is open and may be insecure.")
            found = True
        elif net["security"] == "WEP":
            print(f"- {net['ssid']} uses WEP which is outdated and weak.")
            found = True
    if not found:
        print("- All found networks use modern security protocols.")