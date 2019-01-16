#!/usr/bin/env python

"""
How to Use this File:
	First Run this file on its own, the main function will initialize the Databse file and both tabels
	Then import the function connectDB 
	Additionally import whatever other functions you wish to employ:
		addDB_Vid, addDB_Frame, updateDB_Vid, get_Frames, get_Vid_ID
	Run connectDB at the top of your file to get the cnnct object that is used in both other functions as the first argument
	after that simply us the add or get functions as needed
"""

# This file contains functions which can be called to create and modify a database for the video file uniqueness project
# this file when run on its own will create the initial database and tables, and can be referenced by other python files to easily add and remove data from tables
# the contents of this are based on the tutorial at sqlitetutorial.net
import numpy as np
import os
import sqlite3
from sqlite3 import Error

def connectDB(fName):
	#this is a basic function which will make the database file 
	# this function must be run at the start of the file and it returns cnnct which is used by other functions to connect to the database file
	try:
		cnnct = sqlite3.connect(fName)
		return cnnct
	except Error as e:
		print(e)
	return None

def make_table(cnnct, create_table_sql):
	try:
		c = cnnct.cursor()
		c.execute(create_table_sql)
	except Error as e:
		print(e)

def addDB_Vid(cnnct, newVidName):
	#this function adds a Video to the database
	#this one will create the video data and also two empty frame objects
	#newVidName is the full name and path of the video file
	sql = ''' INSERT INTO  videos(name, chosenFrameID)
			  VALUES(?, 0)'''
	curs = cnnct.cursor()
	curs.execute(sql, (newVidName,))
	# this will return the id of the video
	return curs.lastrowid

def updateDB_Vid(cnnct, target, bestFrame_ID):
	#this function allows one to update the chosenFrameID value in the video, this value is 0 by default 
	#target is the ID of the video in question, bestFrame_ID is the id of the best frame
	sql = ''' UPDATE videos
			  SET chosenFrameID = ?
			  WHERE id = ?'''
	curs = cnnct.cursor()
	curs.execute(sql,(bestFrame_ID, target))

def addDB_Frame(cnnct, vidID, newName, newRedArr, newGrnArr, newBluArr, newReals, newImags):
	#this should update a targeted frame as we create frames when we make videos all 'added' frames done by other programs is actually a matter of updating them
	# in theory the ID of the frame for a given video should have the id of vid_id * 2 + 0 for average and + 1 for unique
	newFrame = []
	#newFrame = newFrame + newRedArr + newGrnArr + newBluArr + newReals + newImags
	newFrame = np.concatenate((vidID, newName, newFrame,newRedArr,newGrnArr,newBluArr,newReals,newImags), axis=None)
	sql = ''' INSERT INTO frames( 
			  	  vid_id, name,
				  red_val_0, red_val_1, red_val_2, red_val_3, red_val_4,
				  grn_val_0, grn_val_1, grn_val_2, grn_val_3, grn_val_4,
				  blu_val_0, blu_val_1, blu_val_2, blu_val_3, blu_val_4,
				  reals_0, reals_1, reals_2, reals_3, reals_4,
				  imags_0, imags_1, imags_2, imags_3,imags_4) 
			  VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'''
	curs = cnnct.cursor()
	curs.execute(sql, newFrame)
	return curs.lastrowid

def get_Frames(cnnct, vid_id):
	#this will return all stored frames associated with a certain video 
	#it should take the form of a list of lists
	curs = cnnct.cursor()
	curs.execute("SELECT * FROM frames WHERE vid_id=?", (vid_id,))
	frameBuf = curs.fetchall()
	return frameBuf

def get_Vid_ID(cnnct, target):
	#this will return all stored info for a video file, searching for it by name
	#it should take the form of a list of lists
	curs = cnnct.cursor()
	curs.execute("SELECT * FROM videos WHERE name=?", (target,))
	frameBuf = curs.fetchone()
	return frameBuf

def file_creation():
	dir_path = os.path.dirname(os.path.realpath(__file__))
	
	db = os.path.join(dir_path, "VFU_DB.db")
	sql_create_video_table = """ CREATE TABLE IF NOT EXISTS videos (
		id integer PRIMARY KEY,
		name text NOT NULL,
		chosenFrameID integer
		); """

	sql_create_frame_table = """CREATE TABLE IF NOT EXISTS frames (
		id integer PRIMARY KEY,
		vid_id integer NOT NULL,
		name text NOT NULL,
		red_val_0 integer NOT NULL,
		red_val_1 integer NOT NULL,
		red_val_2 integer NOT NULL,
		red_val_3 integer NOT NULL,
		red_val_4 integer NOT NULL,
		grn_val_0 integer NOT NULL,
		grn_val_1 integer NOT NULL,
		grn_val_2 integer NOT NULL,
		grn_val_3 integer NOT NULL,
		grn_val_4 integer NOT NULL,
		blu_val_0 integer NOT NULL,
		blu_val_1 integer NOT NULL,
		blu_val_2 integer NOT NULL,
		blu_val_3 integer NOT NULL,
		blu_val_4 integer NOT NULL,
		reals_0 integer NOT NULL,
		reals_1 integer NOT NULL,
		reals_2 integer NOT NULL,
		reals_3 integer NOT NULL,
		reals_4 integer NOT NULL,
		imags_0 integer NOT NULL,
		imags_1 integer NOT NULL,
		imags_2 integer NOT NULL,
		imags_3 integer NOT NULL,
		imags_4 integer NOT NULL,
		FOREIGN KEY (vid_id) REFERENCES videos (id)
	);"""

	con = connectDB(db)
	if con is not None:
		# make our tables
		make_table(con, sql_create_video_table)
		make_table(con, sql_create_frame_table)
	else:
		print("error encountered no database connection")

	return "VFU_DB.db"

# if this file is run on its own it runs main and will create the database file and its tables
if __name__ == '__main__':
	main()
