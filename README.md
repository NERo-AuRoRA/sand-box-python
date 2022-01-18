# sand-box-python
To run the codes from this repository locally you should follow these steps using the command line in your working directory (Windows):

Create a local directory:  
`C:\Users\User> mkdir sand-box-python` 

Go to the new directory:  
`C:\Users\User> cd sand-box-python`  

Clone the remote repository for your local directory:  
`C:\Users\User\sand-box-python> git clone https://github.com/NERo-AuRoRA/sand-box-python.git`  

Now, you need to install the project's dependencies listed in *requirements.txt* using the command:  
`C:\Users\User\sand-box-python> pip install -r requirements.txt`  

> It is interesting that you install the project's dependencies in a [Virtual Env](https://python.land/virtual-environments/virtualenv).

Furthermore, some other dependencies need to be installed manually:
- [Kinect for Windows SDK v1.8](https://www.microsoft.com/en-us/download/details.aspx?id=40278)
- [OpenNI 2 SDK](https://structure.io/openni)  

> When you finish the installation of OpenNI, you must copy the directory *Redist* from *OpenNI2* to *sand-box-python* directory.

To contribute with this project, you should follow these steps in the terminal of your local repository:

Verify what is your current branch:  
`C:\Users\User\sand-box-python> git status`

If your current branch is not *main*:  
`C:\Users\User\sand-box-python> git checkout main`

Now, in branch main, execute:  
`C:\Users\User\sand-box-python> git checkout -b your-branch-name`

When you finish a step from your job, execute:  
`C:\Users\User\sand-box-python> git add .`  
`C:\Users\User\sand-box-python> git commit -m "A message that explains what you did`

When you finish a set of steps that was commited, execute:  
`C:\Users\User\sand-box-python> git push origin your-branch-name`

