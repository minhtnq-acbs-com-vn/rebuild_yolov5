from datetime import date

today = date.today()

moduleRootPath = "./drive"
rootImagePath = "./image"

currentdayImagePath = f"{rootImagePath}/{today}"

tokenFilePath =  f"{moduleRootPath}/credential/token.json"
credentialFilePath = f"{moduleRootPath}/credential/credentials.json"

doneUploadList = []