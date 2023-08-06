#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri June 10 19:25:00 2022

@author: CrisGalvan
"""

import base64
import binascii
import hashlib
import crypt
from sys import breakpointhook

dicFilePath = None
passwdArray = []
passwdDict = {}

def readDicFile(path, appendDic = False):
	"""
	This function creates an array of the different password indicated in the dictionary
	:param path: path of the dictionary with the passwords
	:param appendDic: Specifies whether or not to append the dictionary to the existing one
	:return: boolean
	"""
	readDic = False
	try:
		global passwdArray
		global dicFilePath

		dicFilePath = path
		dicFile = open(path, 'r', encoding='latin-1')
		if not appendDic:
			passwdArray = []

		for passwd in dicFile.readlines():
			line = passwd.replace("\n", "")
			passwdArray.append(line)
		readDic = True
		dicFile.close()
	except FileNotFoundError:
		print("Error: File not found")
	except:
		print("Error while reading the file")
	return readDic

def dictionaryAttackWindows(hashesFile, dictionary = None, appendDic = False):
	"""
	This function performs brute force against the hashes inside the hashesFile file, 
	using the dictionary indicated in the dictionary param.
	:param hashesFile: Path to the file that contains the windows hashes.
	:param dictionary: Path to the file with the password. 
		In case this param is not indicated, the dicFile would be taken as default.
	:param appendDic: Specifies whether to append or not the dictionary
	"""
	try:
		hashes = open(hashesFile, 'r')
	except:
		print('There was an error while opening the file.')
	if not dictionary:
		global dicFilePath
		dictionary = dicFilePath

	# Reading the dictionary and creating the password array with the different passwords
	if not dicFilePath and not dictionary:
		print("Insert a path for the dictionary used for the Brute Force")
		return

	if readDicFile(dictionary, appendDic):
		global passwdDict
		passwdDict = {}
		for account in hashes.readlines():
			passwdFind = False
			acc = account.replace("\n","")
			hash_account = acc.split(':')[3]
			user = acc.split(':')[0]
			print("User: %s Hash: %s" %(acc.split(':')[0], hash_account))
			for passwd in passwdArray:
				# First, it is verified if the password is empty
				if hash_account.lower() == '31d6cfe0d16ae931b73c59d7e0c089C0'.lower():
					passwd = "Empty Password"
					print("[+] Hash found! Username: %s Password: %s\n" %(user, passwd))
					passwdFind = True
					passwdDict[user]=passwd
					break
				ntlm_hash = binascii.hexlify(hashlib.new('md4', passwd.encode('utf-16le')).digest())
				if ntlm_hash.decode("utf-8").lower() == hash_account.lower():
					print("[+] Hash found! Username: %s Password: %s\n" %(user, passwd))
					passwdDict[user] = passwd
					passwdFind = True
					break
			if not passwdFind:
				print("[-] Password not found. Add another dictionary to try again\n")

	hashes.close()


def dictionaryAttackUnix(hashesFile, dictionary = None, appendDic = False):
	"""
        This function performs brute force against the hashes inside the hashesFile file,
		 using the dictionary indicated in the dictionary param.
        :param hashesFile: Path to the file that contains the linux hashes.
        :param dictionary: Path to the file with the password. 
			In case this param is not indicated, the dicFile would be taken as default.
		:param appendDic: Specifies whether to append or not the dictionary
        """
	hashes = open(hashesFile, 'r')
	if not dictionary:
		global dicFilePath
		dictionary = dicFilePath

	# Reading the dictionary and creating the password array with the different passwords
	if not dicFilePath and not dictionary:
		print("Insert a path for the dictionary used for the Brute Force")
		return
	if readDicFile(dictionary, appendDic):
		global passwdDict
		passwdDict = {}
		for line in hashes.readlines():
			passwdFind = False
			caracteristics = line.split(':')
			username = caracteristics[0]
			hash = caracteristics[1].split('$')
			hashType = hash[1]
			salt ='$'+hashType+'$'+ hash[2]
			passwdDigest = hash[3]

			if hashType == '6':
				hashTypeStr = 'SHA-512'
			elif hashType == '5':
				hashTypeStr = 'SHA-256'
			elif hashType == '2' or hashType == '2a':
				hashTypeStr = 'Blowfish' 
			elif hashType == '1':
				hashTypeStr = 'MD5'

			print('[+] Hash type '+hashTypeStr+' for user '+username)
			for passwd in passwdArray:
				cryptWord = crypt.crypt(passwd, salt)
				digest = cryptWord.split('$')[3]
				if digest == passwdDigest:
					print('[+] Found password %s for the user %s\n' %(username, passwd))
					passwdDict[username] = passwd
					passwdFind = True
					break
			if not passwdFind:
				print('[-] Password not found for the user '+username+'\n')
	hashes.close()


dictionaryAttackWindows('../../TFM_docs/hashes', '../../TFM_docs/dict')
