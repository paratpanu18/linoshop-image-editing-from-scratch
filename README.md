# 🖼️ Linoshop - Image Editing Software from Scratch
Linoshop is a lightweight image editing software developed from the ground up, leveraging core concepts from linear algebra to provide fundamental image processing features. Using mathematical techniques such as linear transformations, matrix operations, and convolutions, Linoshop enables users to apply basic yet effective image edits in real time.

## 📑 Prerequisites
Python 3.12 or later
Earlier versions of Python may not be compatible or supported.
## ⬇️ Installation Guide
1. Create a Python Virtual Environment
Start by creating a Python virtual environment using `venv`. This step ensures that you have an isolated environment with the required dependencies.
```bash
python -m venv .venv
```

2. Activate the Virtual Environment
On Windows:
```bash
.venv\Scripts\activate.ps1
```
> Note: On Windows, you may need to enable script execution by setting the execution policy. Run the following command in PowerShell:

```bash
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

On UNIX-based Operating Systems (Linux/macOS):

```bash
source .venv/bin/activate
```

If the virtual environment is successfully activated, you’ll see `(venv)` appear at the beginning of your command line prompt, indicating that you're working within the isolated environment.

3. Install Dependencies
With the virtual environment activated, install the required dependencies listed in the requirements.txt file.

```bash
pip install -r requirements.txt
```

4. Run the Application
Once the dependencies are installed, you can run the application by executing the following command:

```bash
python src/main.py
```
Linoshop will now be up and running, ready to process and edit your images using powerful linear algebra techniques.
