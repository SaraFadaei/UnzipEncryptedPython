# UnzipEncryptedPython
## Unzip the password protected files useing azure function app and python as run stack

- Create a new project in VS Code, connect VS Code to Azure subscription using Azure Extension and credentials.

- Install Python version 3.*

- Create a new function in the workspace using the HTTP trigger template and the latest version of Python (currently 3.10).

- Add the azure-functions and azure-storage-blob modules to the Python requirements.txt file

- Write the Python code to unzip a password-protected ZIP file using the connection to the storage account connection string and the container that contains the ZIP file.

- Run the code locally and run the function in the workspace to test the code's functionality.

- Deploy and run the function in an Azure Function app after providing the body request.

- Create a key vault resource that stores the password as a secret.

- Create and set up a pipeline in Synapse using web activity and Azure function activity to get the password from the key vault using secret identifiers and managed identity application ID values and connect the Azure function link service to the function using the function key.

- Set the Secure Output option to true to prevent the secret value from being logged in plain text. Any further activities that consume this value should have their Secure Input option set to true.

