from Google import Create_Service
from googleapiclient import errors
import datetime
import os

class assessments():

    def __init__(self):
        #authenticate credentials and setup the service interaction
        CREDENTIALS = "credentials.json"
        API_NAME = "drive"
        API_VERSION = "v3"
        SCOPES = ["https://www.googleapis.com/auth/drive"]
        global service

        try:
            service = Create_Service(CREDENTIALS, API_NAME, API_VERSION, SCOPES)
        except errors.HttpError as error:
            print("Unable to successfully authenticate credentials \n")
            print(error.content)



    def assessment1(self,source, folderid = None):
        """
        Calling function to returns the number of files and folders from a google drive folder

        Given a google drive folder id(source), generate a report in the current
        current working directory which displays the number of files and folders
        within the source folder.

        Optionally: Displays the number of files and folders for each folder under
        folderid

        Parameters:
        source (string): Google folder id of the source directory.

        folderid (string): Google folder id; Begin logging the number of files
        and folders for each folder under this folder id

        Returns:
        Generates report in current working directory

        """

        #Check if source is a folder if not raise exception
        try:
            sourceMetadata = service.files().get(fileId=source).execute()
            if sourceMetadata.get("mimeType") != "application/vnd.google-apps.folder":
                raise Exception("source id does not map to a googlde drive folder")
            #Check if folderid is a folder if not raise exception
            if folderid != None:
                folderidMetadata = service.files().get(fileId=folderid).execute()
                if folderidMetadata.get("mimeType") != "application/vnd.google-apps.folder":
                    raise Exception("folderid does not map to a googlde drive folder")

        except errors.HttpError as error:
            # The API encountered a problem.
            print("Unable to generate Google Drive Report \n")
            print("API Encountered a problem \n")
            print(error.content)



        #Using recursion, will need to store values in mutuble object
        numFolders = [0]
        numFiles = [0]
        flat_list = []

        #folderid is an optional paramters for reusability
        if folderid != None:
            #call assessment1helper and log the number files and folders for each folder under folderid
            self.assestment1helper(source, numFolders, numFiles, folderid, flat_list, found=False)
        else:
            #call assessment1helper without logging files and folders for each folder under folderid
            self.assestment1helper(source, numFolders, numFiles, folderid=None, flat_list=None, found=None)



        #create a file name Report with current timestamp
        timestamp = str(datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S"))
        reportFilename = "Report_" + timestamp + ".txt"
        file = open(reportFilename, "w")
        line = "Report Generated at " + timestamp + "\n\n"
        file.write(line)


        #capture lines for multiline write
        line1 = "Source Folder ID: " + str(source) + "\n"
        line2 = "Number of Sub Folders: " + str(numFolders[0]) + "\n"
        line3 = "Number of Files: " + str(numFiles[0]) + "\n"
        line4 = "\n"
        file.writelines([line1, line2, line3, line4])

        #print lines to monitor
        print(line1)
        print(line2)
        print(line3)
        print(line4)

        #donwstream reporting under a folder is enabled
        if folderid != None:
            line = "Number of files and folders for each folder under Folder ID: \n" + str(folderid)
            print(line)
            file.write(line)
            for folderinfo in reversed(flat_list):
                #capture lines for multiline write
                line1 = "Folder Name: " + str(folderinfo[0] + "\n")
                line2 = "\t" + "Number of Folders: " + str(folderinfo[1]) + "\n"
                line3 = "\t" + "Number of Files: " + str(folderinfo[2]) + "\n"
                line4 = "\n"
                file.writelines([line1, line2, line3, line4])

                #print to monitor
                print(line1)
                print(line2)
                print(line3)
                print(line4)

        line = "---------- Report Complete ----------\n"
        file.write(line)
        print("Report located at: {}".format(os.path.join(os.getcwd(),reportFilename)))

    def assestment1helper(self,source, numFolders, numFiles, folderid, flat_list, found):

        """
        Helper function to return the number of files and folders from a google drive folder

        Given a google drive folder id(source), generate a report in the current
        current working directory which displays the number of files and folders
        within the source folder.

        Optionally: Displays the number of files and folders for each folder under
        folderid

        Parameters:
        source (string): Google folder id of the source directory.

        numFolders(list): Mutuable array of lenfth 1 to count the values of folders

        numFiles(list): Mutuable array of lenfth 1 to count the values of folders

        folderid (string): Google folder id; Begin logging the number of files
        and folders for each folder under this folder id

        flat_list(list): List of folder information([specific folder name, the
        number of folders this folder has,the number of files this folder has]])

        found(boolean): True: folderid has been found. Logging is taking place
                        False:folderid has not been found. No logging is taking place
        Returns:
        Number of folders in 0th position of numFolders
        Number of files in 0th position of numFiles
        List of folder information inside flat_list


        """

        #caputer number of files and folders for this folder
        myfolderCount = 0
        myfilesCount = 0

        #array to capture all folder or file reponse bodies
        filesFolderslist = list()

        try:
            #parameter to query a particular folder
            query = f"parents='{source}'"

            #get the response body(dict) that has the list of folders and files for the source
            #see example of reposne body: https://developers.google.com/drive/api/v3/reference/files/list
            response = service.files().list(q=query).execute()

            #get the metadata for this source
            #see example of metadata: https://developers.google.com/drive/api/v3/reference/files
            fileMetadata = service.files().get(fileId=source).execute()

        except errors.HttpError as error:
            # The API encountered a problem.
            print("Unable to generate Google Drive Report \n")
            print("API Encountered a problem \n")
            print(error.content)

        #list of files and folders from response
        filesFolderslist = response.get('files')

        #file and folder name from response
        folderName = fileMetadata.get('name')
        fileid = fileMetadata.get('id')

        #check is this folder from metadata and paramter from folder
        #are the same to begin capturing file and folder information
        if fileid == folderid:
            found = True

        #check if the nextPageToken is in the response body, if so
        #the api has more data to retrieve. Rerun the above calls to
        #get the response body(dict) that has the list of folders and files for the source.
        #Otherwise break or do not enter loop
        nextpageToken = response.get('nextPageToken', None)
        while nextpageToken:
            try:
                response = service.files().list(q=query).execute()

            except errors.HttpError as error:
                # The API encountered a problem.
                print("Unable to generate Google Drive Report \n")
                print("API Encountered a problem \n")
                print(error.content)


            filesFolderslist.extend(response.get('files'))
            nextpageToken = response.get('nextPageToken', None)

        #iterate thru the list of files and folders for THIS folder
        for file_attributes in filesFolderslist:
            #if the file type is folder increment the overall number of folders(numFolders[0])
            #if this is the target folder to log downstream file and folder information
            #found will be true. increment folder(myfolderCount) and file(myfilesCount)
            #count for THIS folder
            #recrusively call assessment1helper for all folders
            if file_attributes.get("mimeType") == "application/vnd.google-apps.folder":
                #increment number of folders if this a folder
                numFolders[0] +=1
                if found == True:
                    myfolderCount +=1
                #recurisve call to assessment1helper for this folder
                self.assestment1helper(file_attributes.get("id"),numFolders,numFiles,folderid, flat_list, found)
            else:
                numFiles[0] +=1
                if found == True:
                    myfilesCount +=1

        #create a tuple [this folder name, the number of folders this folder has,
        #the number of files this folder has] add this tuple to the list to display and report
        if found == True:
            flat_list.append([folderName,myfolderCount,myfilesCount])




    def assessment2(self,source,folderid=None):
        """
        Returns the number of files and folders under a Google Drive directory
        Returns the number of nested folders from a Google Drive directory

        Generates a report to show the number of nested folders within the source folder.

        Generates a report to show the number of number of files and folders under each
        folder within a Google Drive directory

        Parameters:
        source (string): Google folder id of the source directory.

        folderid (string): Google folder id; Begin logging the number of files
        and folders for each folder under this folder id

        Use Case 1:
        If folderid is None the report will show the number of nested folders
        inside source and the number of files and folders under source.

        Use Case 2:
        If folderid is given. Report will show the number of nested folders
        inside source and the number of number of files
        and folders under folderid

        Returns:
        Generates report in current working directory

        """
        if folderid ==None:
            #use case 1 run assessment1 gathering information about source
            return self.assessment1(source, source)
        else:
            #use case 2 run assessment1 gathering information about
            #nested folders in source and files and folder info for each
            #folder in folderid
            return self.assessment1(source, folderid)


    def assessment3(self,source, destination):
        """
        Calling function to copy content from google drive source folder to google drive destination folder.

        Copies content from google drive source folder to google drive destination folder.
        Maintains directory structure, files and fodler attributes excluding parent and
        file/folder ids

        Parameters:
        source (string): Google folder id of the source directory.

        destination(string): Google folder id of the destination directory.

        Returns:
        None

        """

        try:
            #Check if both source and destination have values
            if not source or not destination:
                raise Exception("Make sure the source or destination is populated correctly")

            #Check if source is a folder if not raise exception
            sourceMetadata = service.files().get(fileId=source).execute()
            if sourceMetadata.get("mimeType") != "application/vnd.google-apps.folder":
                raise Exception("source id does not map to a googlde drive folder")

            #Check if destination is a folder if not raise exception
            destinationMetadata = service.files().get(fileId=destination).execute()
            if destinationMetadata.get("mimeType") != "application/vnd.google-apps.folder":
                raise Exception("folderid does not map to a googlde drive folder")

        except errors.HttpError as error:
            # The API encountered a problem.
            print("API Encountered a problem \n")
            print(error.content)



        print("Copiying contents from Source Folder ID: {} to Detsination Folder ID: {}".format(source, destination))
        print("\n")
        #call assessment3 helper function
        self.assessment3helper(source, destination)
        print("Successfully copied contents from Source Folder ID: {} to Destination Folder ID: {}".format(source, destination))



    def assessment3helper(self,source, destination):
        """
        Helper function to copy content from google drive source folder to google drive destination folder.

        Copies content from google drive source folder to google drive destination folder.
        Maintains directory structure, files and folder attributes excluding parent and
        file/folder ids

        Parameters:
        source (string): Google folder id of the source directory.

        destination(string): Google folder id of the destination directory.

        Returns:
        None

        """

        try:

            #parameter to query a particular folder
            query = f"parents='{source}'"

            #get the response body(dict) that has the list of folders and files for the source
            #see example of reposne body: https://developers.google.com/drive/api/v3/reference/files/list
            response = service.files().list(q=query).execute()


            #get the metadata for the source
            #see example of metadata: https://developers.google.com/drive/api/v3/reference/files
            sourceMetadata = service.files().get(fileId=source).execute()

        except errors.HttpError as error:
            # The API encountered a problem.
            print("API Encountered a problem \n")
            print(error.content)

        #creating the metadata for a new folder
        #use the same metadata from source folder
        destinationMetadata = dict(sourceMetadata)

        #add parent field with destination as value to point to
        #parent folder of this newly created folder
        destinationMetadata['parents'] = [destination]

        #remove current file/folder id
        #this value will be auto-generated by the create() api
        del destinationMetadata['id']

        #api call to create folder with parent being the destination.
        #see example https://developers.google.com/drive/api/v3/folder
        createNewfolder = service.files().create(body=destinationMetadata, fields = 'id').execute()

        #hold the value of the new folder id
        newFolderId = createNewfolder['id']

        #list of files and folders from response
        filesFolderslist = response.get('files')

        #check if the nextPageToken is in the response body, if so
        #the api has more data to retrieve. Rerun the above calls to
        #get the response body(dict) that has the list of folders and files for the source.
        #Otherwise break or do not enter loop
        nextpageToken = response.get('nextPageToken', None)

        while nextpageToken:
            try:
                response = service.files().list(q=query).execute()

            except errors.HttpError as error:
                # The API encountered a problem.
                print("Unable to generate Google Drive Report \n")
                print("API Encountered a problem \n")
                print(error.content)


            filesFolderslist.extend(response.get('files'))
            nextpageToken = response.get('nextPageToken', None)

        #iterate thru the list of files and folders for THIS folder

        #if this is the target folder to log downstream file and folder information
        #then found will be true.
        #increment folder(myfolderCount) and file(myfilesCount) for THIS folder
        #recrusively call assessment1helper for all folders
        for file_attributes in filesFolderslist:
            #if the file type is folder recrusively call assessment1helper
            if file_attributes.get("mimeType") == "application/vnd.google-apps.folder":
                self.assessment3helper(file_attributes.get("id"),newFolderId)
            #if the file type is nto a  folder
            else:
                #creating new metadata for a new file
                #using the same metadata from file
                copiedFilemetaData = dict(file_attributes)
                #add parent field with destination as value to point to
                #parent folder of this newly created file
                copiedFilemetaData['parents'] = [newFolderId]
                #remove current file/folder id
                #this value will be auto-generated by the copy() api
                del copiedFilemetaData['id']
                #api call to copy file see example: https://developers.google.com/drive/api/v3/reference/files/copy
                service.files().copy(fileId=file_attributes.get("id"), body=copiedFilemetaData).execute()
