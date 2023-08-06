PASSWORD CRACKER
==============

This package has been developed to obtain, in a faster way, operating system users by using a dictionary and the OS hash dump. It can be either use for a Windows OS and for a Unix OS.

The readDicFile(path, appendDic) returns a boolean, True if everything went well and False either way. This function reads a file stored at 'path', and can append the passwords in that file to the ones that the user has previously stored.

The dictionaryAttackWindows(hashesFile, dictionary, appendDic) does not return anything. This function performs the dictionary attack to a Windows hashes file, using the dictionary indicated by the user, or another one indicated before. Whenever a password matches, it's stored in a global variable called passwdDict. This variable is set to an empty dictionary every time an attack is performed.

The function dictionaryAttackUnix(hashesFile, dictionary, appendDic) does not return any value. As the previous function, it performs a dictionary attack to a Unix hashes file, using the indicated dictionary or a previous one. All the passwords that are found are stored in the global variable passwdDict.