from bunnyhop import BunnyClient

def main():
    # BURAYA KENDİ API KEY'İNİZİ GİRİN
    API_KEY = "YOUR-BUNNY-API-KEY-HERE"
    
    if API_KEY == "YOUR-BUNNY-API-KEY-HERE":
        print("Please open the file and edit the API_KEY variable!")
        return

    client = BunnyClient(API_KEY)
    
    try:
        print("--- Zone List ---")
        zones = client.zone.list()
        for z in zones:
            print(f"- {z.name} ({z.id}) -> {z.origin_url}")
            
        print("\n--- Storage List ---")
        storage_zones = client.storage.list()
        for s in storage_zones:
            print(f"- {s.name} (Region: {s.region})")
            
        # Example: Upload a file to the first storage zone
        if storage_zones:
            target = storage_zones[0]
            print(f"\n--- '{target.name}' into the file is being uploaded... ---")
            
            # Create a dummy file content
            dummy_content = b"Hello Bunny.net!"
            
            # Upload
            client.storage.upload_file(target, "test-folder/", "hello.txt", dummy_content)
            print("Upload successful!")
            
            # Download
            downloaded = client.storage.download_file(target, "test-folder/", "hello.txt")
            print(f"Downloaded content: {downloaded.decode('utf-8')}")
            
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    main()
